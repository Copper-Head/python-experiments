"""
DCI proof of concept
Context is a separate object to the Collaboration (again for exploration of alternatives).
Made a class for it, but a Dictionary is also possible.

Author: David Byers, Serge Beaumont
7 October 2008

N.B.
Adapted to run on python 3.
"""
import types


class Role:
    """A role is a special class that never gets instantiated directly.
    instead, when the user wants to create a new role instance, we create a new class that
    hast the role and another object's class as its superclasses, then create an instance of that class,
    and link the new object's dict to the original object's dict.
    """
    def __new__(cls, ob):
        c = types.new_class(cls.__name__, bases=(cls, ob.__class__))
        inst = super().__new__(c)
        inst.__dict__ = ob.__dict__
        return inst

    def __init__(self, ob):
        """Do not call the superclass __init__. If we did then we would call the __init__ function
        in the real class hierarchy too (i.e. Account, in this example).
        """
        pass

    def __getattr(self, attr):
        """Proxy to object"""
        return getattr(self.__ob__, attr)

    def __setattr(self, attr, value):
        setattr(self.__ob__, attr, value)

    def __delattr(self, attr):
        delattr(self.__ob__, attr)


class MoneySource(Role):
    def transfer_to(self, ctx, amount):
        if self.balance >= amount:
            self.decreaseBalance(amount)
            ctx.sink.receive(ctx, amount)


class MoneySink(Role):
    def receive(self, ctx, amount):
        self.increaseBalance(amount)


class Account:
    """The class for the domain object."""
    def __init__(self, amount):
        print ( 'Creating a new account with balance of' + str(amount) )
        self.balance = amount
        super(Account, self).__init__()

    def decreaseBalance(self, amount):
        print ( 'Withdraw ' + str(amount) + 'from ' + str(self) )
        self.balance -= amount

    def increaseBalance(self, amount):
        print ( 'Deposit ' + str(amount) + 'in ' + str(self) )
        self.balance += amount


class Context:
    """Holds context state."""
    pass


class TransferMoney:
    """This is the environment, like the controller, that binds the context and offers an interface to
    trigger the context to run.
    """
    def __init__(self, source, sink):
        self.context = Context()
        self.context.source = MoneySource(source)
        self.context.sink = MoneySink(sink)

    def __call__(self, amount):
        self.context.source.transfer_to(self.context, amount)

if __name__ == '__main__':
    src = Account(1000)
    dst = Account(0)
    t = TransferMoney(src, dst)
    t(100)
    print(src.balance)
    print(dst.balance)
