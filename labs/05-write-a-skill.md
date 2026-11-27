# Lab 05: write a skill

1. Pick something you did twice in labs 02 to 04.
2. Run `/new-skill <what it is>`. Put it in a group folder (create `skills/<tool>/` if the tool is new).
3. Read the generated skill. Remove anything you did not verify or mark it `unverified`.
4. `python scripts/quick_validate.py skills/<group>/<name>` and `python scripts/sync_agent_folders.py`.
5. Start a new chat and ask for the task. Does the agent use the skill?

A good skill: a clear "use when" description, steps, rules, typical errors, under about 60 lines.
