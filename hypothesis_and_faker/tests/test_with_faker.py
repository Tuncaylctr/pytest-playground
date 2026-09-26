from faker import Faker

from uc.converter import ConversionGraph, Quantity


@pytest.fixture(
    scope="class",
    params=["bfs", "dfs"]
)
def unit_registry(request) -> ConversionGraph:
    g = ConversionGraph(search_algo=request.param)

    g.add_unit("m", "length")
    g.add_unit("cm", "length")
    g.add_unit("mm", "length")
    g.add_unit("mi", "length")
    g.add_unit("km", "length")

    g.add_linear("m", "cm", scale=100.0)
    g.add_linear("cm", "mm", scale=10.0)
    g.add_linear("mi", "km", scale=1.60934)

    return g

def test_linear_forward_and_inverse(unit_registry):
    faker = Faker()

    for _ in range(10):
        meters = faker.pyfloat(left_digits=2, right_digits=3, positive=True)
        print(f'{meters=}')

        m_init = Quantity(meters, "m")
        mm = unit_registry.convert(m_init, "mm")
        m_back = unit_registry.convert(mm, "m")
        assert m_back.value == pytest.approx(meters, rel=1e-12)



