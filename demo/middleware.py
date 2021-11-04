from whitenoise.middleware import WhiteNoiseMiddleware


class DemoMiddleware(WhiteNoiseMiddleware):
    def immutable_file_test(self, path, url):
        name = url[len(self.static_prefix) :]
        if name.startswith('demo/'):
            return True
        return super().immutable_file_test(path,url)