from typing import NewType, TypedDict, DefaultDict
from typing import Generic, TypeVar, List

T = TypeVar("T")


class DateDictType(TypedDict):
    end: str | None
    start: str | None
    time_zone: str | None


class DateType(TypedDict):
    date: DateDictType
    id: str
    type: str


# type dateType = dict[
#     "date" : dict["end" : str | None, "start" : str | None, "time_zone" : str | None]
#     | None,
#     id:str,
#     type:"date",
# ]
# TODO: add check for the start and end that the strings are iso


class CheckboxType(TypedDict):
    checkbox: bool
    id: str
    type: str


# type checkboxType = dict["checkbox":bool, id:str, "type":"checkbox"]

# NewType("CheckboxType", checkboxType)

# type mutliSelectItem = dict["color":str, id:str, "name":str]

# type multiSelectType = dict[
#     id:str, "mutli_select" : [] | mutliSelectItem, "type":"mutli-select"
# ]
# NewType("MultiSelectType", multiSelectType)


class MultiSelectDictType(TypedDict):
    color: str
    id: str
    name: str


class MutliSelectType(TypedDict):
    id: str
    multi_select: DefaultDict | MultiSelectDictType


# type lastEditedTimeType = dict[
#     id:str, "last_edited_time":str, "type":"last_edited_time"
# ]
# # TODO: add check for lasteditedtime that string is iso
# NewType("LastEditedTimeType", lastEditedTimeType)


class LastEditedTimeType(TypedDict):
    id: str
    last_edited_time: str
    type: str


# type nameType = dict[
#     id:"title",
#     "title" : list[
#         "annotations" : dict[
#             "bold":bool,
#             "code":bool,
#             "color":str,
#             "italic":bool,
#             "strikethrough":bool,
#             "underline":bool,
#         ],
#         "href" : str | None,
#         "plain_text" : str | None,
#         "text" : {"content": str | None, "link": str | None},
#         "type":"text",
#     ],
#     "type":"title",
# ]


class AnnotationsType(TypedDict):
    bold: bool
    code: bool
    color: str
    italic: bool
    strikethrough: bool
    underline: bool


class TextType(TypedDict):
    content: str | None
    link: str | None


class TitleInfoType(TypedDict):
    annotations: AnnotationsType
    href: str | None
    plain_text: str | None
    text: TextType
    type: str


class NameType(TypedDict):
    id: str
    title: List[TitleInfoType]
    type: str


class RichTextType(TypedDict):
    id: str
    rich_text: List[TitleInfoType]
    type: str


class IdType(TypedDict):
    id: str


class RelationType(TypedDict):
    has_more: False
    id: str
    relation: DefaultDict | IdType
    type: str


class SelectType(TypedDict):
    id: str
    select: MultiSelectDictType | None
    type: str


class NotionPropsType(TypedDict):
    Date: DateType
    Deadline: DateType
    Done: CheckboxType
    Label: MutliSelectType
    Name: NameType
    Parent: RelationType
    Priority_Level: SelectType
    Project: SelectType
    Section: SelectType
    ToDoistId: RichTextType
