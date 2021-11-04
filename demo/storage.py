import collections

from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

from whitenoise.storage import HelpfulExceptionMixin


class DemoFilesStorage(HelpfulExceptionMixin, ManifestStaticFilesStorage):
    """
    Don't process files compiled by front-end build tools
    based on: https://joseph.is/3q3WDMc
    """
    _skip_patterns = ['demo/',]

    def get_skip_patterns(self):
        return tuple(self._skip_patterns)

    def post_process(self, paths, dry_run=False, **options):
        """ Skip files generated hashed by webpack. """

        if dry_run:
            return

        unhashed_paths = {}
        for path, path_info in paths.items():
            if path.startswith(self.get_skip_patterns()):
                yield path, None, False
            else:
                unhashed_paths[path] = path_info

        yield from super().post_process(
            unhashed_paths, dry_run=dry_run, **options)


    def stored_name(self, name):

        if name.startswith(self.get_skip_patterns()):
            return name
        else:
            return super().stored_name(name)
