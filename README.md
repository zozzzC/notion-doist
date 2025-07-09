# notion-doist

A Python script that 2-way syncs your Notion and Todoist tasks and pages.

--

Features:

- Sync Projects, Sections, Priorities, Parent/Child Tasks, and Labels between a Notion Database and Todoist!
- Synced tasks/pages are updated between Notion and Todoist.
- Projects and Sections are created and synced between Notion and Todoist.
- Support for deleted and completed tasks/pages.

--

Setup (Important):

- Your Notion database must look like this (case sensitive):
- ![[Pasted image 20250709120305.png]]
- Fields:
  - Done (Checkbox)
  - Name (Title)
  - Priority (Single Select with fields High, Medium, Low)
  - Project (Single Select)
  - Section (Single Select)
  - Date (Date)
  - Deadline (Date)
  - Label (Mutli Select)
  - Last edited time (Last edited time)
  - ToDoistId (Rich Text)
  - Parent (**Two Way Relation** to the same database)
  - Child (**Two Way Relation** to the same database -- this is related to Parent.)
- In the main directory, change config.example.json to config.example. We will now configure our files.
- [Create an API key with Notion](https://developers.notion.com/docs/create-a-notion-integration) and store the API secret in the notion_token field.
  - Connect the API with your Notion database by going under Connections. Allow the API to read and write.
- Get your Notion database URL and store in the notion_db_url field.
- Get your [Notion database ID](https://stackoverflow.com/questions/67728038/where-to-find-database-id-for-my-database-in-notion) and store in the noiton_db_id field.
- [Create an API key](https://www.todoist.com/help/articles/find-your-api-token-Jpzx9IIlB) with Todoist and store the API secret in the todoist_token field.
- [ Find your timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) and paste the string into the timezone field. (Use the 'TZ identifier' string. EG: If my timezone is +00:00, I would use 'Africa/Abidjan' as the timezone string.)
- When finished, simply run main.py.

--

Known Limitations:

- Recurring tasks are not supported.
- Whole day tasks in Todoist/Notion are synced to be tasks at 12:00AM in Notion/Todoist respectively.
- Please note that the code has not yet been finalised! Bug fixes and optimisations are on the way, but the script does work.
