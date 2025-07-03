type dateType = dict[
    "date" : dict["end" : str | None, "start" : str | None, "time_zone" : str | None]
    | None,
    id:str,
    type:"date",
]
# TODO: add check for the start and end that the strings are iso


type checkboxType = dict["checkbox":bool, id:str, "type":"checkbox"]

type mutliSelectItem = dict["color":str, id:str, "name":str]

type multiSelectType = dict[
    id:str, "mutli_select" : [] | mutliSelectItem, "type":"mutli-select"
]

type lastEditedTimeType = dict[
    id:str, "last_edited_time":str, "type":"last_edited_time"
]
# TODO: add check for lasteditedtime that string is iso

# type numberType = dict[]

type nameType = dict[
    id:"title",
    "title" : list[
        "annotations" : dict[
            "bold":bool,
            "code":bool,
            "color":str,
            "italic":bool,
            "strikethrough":bool,
            "underline":bool,
        ],
        "href" : str | None,
        "plain_text" : str | None,
        "text" : {"content": str | None, "link": str | None},
        "type":"text",
    ],
    "type":"title",
]

type richTextType = dict[
    id:"title",
    "rich_text" : list[
        "annotations" : dict[
            "bold":bool,
            "code":bool,
            "color":str,
            "italic":bool,
            "strikethrough":bool,
            "underline":bool,
        ],
        "href" : str | None,
        "plain_text" : str | None,
        "text" : {"content": str | None, "link": str | None},
        "type":"text",
    ],
    "type":"rich_text",
]

type idType = dict["id":str]


type relationType = dict[
    "has_more":bool,
    id:str,
    "relation" : [] | idType,
    "type":"relation",
]


type selectType = dict["id":str, "select" : mutliSelectItem | None, "type":"select"]

type notionPropsType = dict[
    "Date":dateType,
    "Deadline":dateType,
    "Done":checkboxType,
    "Label":multiSelectType,
    "Name":nameType,
    "Parent":relationType,
    "Priority Level":selectType,
    "Project":selectType,
    "Section":selectType,
    "ToDoistId":richTextType,
]

type pagesType = dict[
    str,
    dict[
        "Date" : dict[
            "end" : str | None, "start" : str | None
        ]
        | None,
        "Deadline" : dict[
            "end" : str | None, "start" : str | None
        ]
        | None,
        "Label": dict[str] | [],
        "Name": str,
        "ParentId": str | None, 
        "Priority_Level": str,
        "Project": str,
        "Section": str,
        "ToDoistId": str | None,
        "Status": bool
    ],
]
