"""Boolean logic gate for combining two boolean signals."""

from comfy_api.latest import io


class ImgUtilsBoolLogic(io.ComfyNode):
    """Combine two boolean signals with a selectable logic operation."""

    OPS = ["AND", "OR", "XOR", "NAND", "NOR"]

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsBoolLogic",
            display_name="Imgutils Boolean Logic",
            category="imgutils/utility",
            description=(
                "Combine two boolean signals with a logic gate — "
                "AND, OR, XOR, NAND, and NOR operations."
            ),
            search_aliases=["boolean", "logic", "and", "or", "not", "gate", "combine", "condition"],
            inputs=[
                io.Boolean.Input(
                    "a",
                    default=False,
                    tooltip="First boolean signal.",
                ),
                io.Boolean.Input(
                    "b",
                    default=False,
                    tooltip="Second boolean signal.",
                ),
                io.Combo.Input(
                    "op",
                    options=cls.OPS,
                    tooltip="Logic operation to apply.",
                ),
            ],
            outputs=[
                io.Boolean.Output(display_name="result"),
            ],
        )

    @classmethod
    def execute(cls, a, b, op) -> io.NodeOutput:
        ops = {
            "AND": lambda a, b: a and b,
            "OR": lambda a, b: a or b,
            "XOR": lambda a, b: a != b,
            "NAND": lambda a, b: not (a and b),
            "NOR": lambda a, b: not (a or b),
        }
        return io.NodeOutput(ops[op](a, b))
