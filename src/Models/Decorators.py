class GetErros:
    errors = []
    def get_error(self,function):
        def wrapper(*args):
            try:
                x = function(*args)
                return x
            except Exception as e:
                method_name = str(function)
                log_error = (e,method_name[10:])
                self.register_error(log_error)
        return wrapper

    def register_error(self,erro):
        self.errors.append(erro)

    def clean_list(self):
        self.errors.clear()