from magia import Input, Module, Output


class TestModSpecialize:
    def test_module_anonymous_init(self):
        class SubModule(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

                self.io += Input("d", 8)
                self.io += Output("q", 8)

                self.io.q <<= self.io.d

        class TopModule(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

                self.io += Input("d", 8)
                self.io += Output("q1", 8)
                self.io += Output("q2", 8)
                self.io += Output("q3", 8)

                SubModule().instance(io={
                    "d": self.io.d,
                    "q": self.io.q1,
                })
                SubModule().instance(io={
                    "d": self.io.d,
                    "q": self.io.q2,
                })
                SubModule().instance(io={
                    "d": self.io.d,
                    "q": self.io.q3,
                })

        result = Module.elaborate_all(TopModule(name="top_module"))
        assert len(result) == 4, f"Expected 4 modules: Top + 3 SubModules, got {len(result)} modules."

    def test_reuse_specialized_module(self):
        class SubModule(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

                self.io += Input("d", 8)
                self.io += Output("q", 8)

                self.io.q <<= self.io.d

        class TopModule(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

                self.io += Input("d", 8)
                self.io += Output("q1", 8)
                self.io += Output("q2", 8)
                self.io += Output("q3", 8)

                specialized = SubModule()
                specialized.instance(io={
                    "d": self.io.d,
                    "q": self.io.q1,
                })
                specialized.instance(io={
                    "d": self.io.d,
                    "q": self.io.q2,
                })
                specialized.instance(io={
                    "d": self.io.d,
                    "q": self.io.q3,
                })

        result = Module.elaborate_all(TopModule(name="top_module"))
        assert len(result) == 2, f"Expected 2 modules: Top + 1 SubModules, got {len(result)} modules."
