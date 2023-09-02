from src.basemodels import ImmutableModel


def test_immutable_new() -> None:
    """
    Tests the working of new method.
    Multiple scenarios and deeper reference checks are yet to be added.
    :return:
    """

    class A(ImmutableModel):
        arg1: int
        arg2: tuple[str, ...]

    class B(ImmutableModel):
        a: A
        arg2: float = 2.2

    class C(ImmutableModel):
        b: B

    class D(ImmutableModel):
        c: C

    # TODO Implement factory pattern
    d = D(c=C(b=B(a=A(arg1=4, arg2=("a", "b", "c")))))

    assert d.c.b.arg2 == 2.2

    d_with_nested_b_arg2_as_4_4 = d.new(key="c.b.arg2", value=4.4)

    assert d_with_nested_b_arg2_as_4_4.c.b.arg2 == 4.4
