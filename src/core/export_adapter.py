from ..helper.auto_numbered import AutoNumberedEnum


__all__ = ["ExportAdapterFormat", "ExportAdapter"]


class ExportAdapterFormat(AutoNumberedEnum):
    TXT = ()


class ExportAdapter:
    def __init__(self, path: str = "a.out") -> None:
        self.__path = path

    def export(self, data: str, format: ExportAdapterFormat = ExportAdapterFormat.TXT) -> None:
        if format == ExportAdapterFormat.TXT:
            with open(self.__path, "a", encoding="utf-8") as f:  # add to file
                f.write(data)
        else:
            raise NotImplementedError(f"Export format {format} is not supported.")
