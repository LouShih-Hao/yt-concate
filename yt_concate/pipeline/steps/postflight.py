from .step import Step


class Postflight(Step):
    def process(self, data, inputs, utils):
        print('in Postflight')
        if inputs['cleanup']:
            utils.delete_dirs()