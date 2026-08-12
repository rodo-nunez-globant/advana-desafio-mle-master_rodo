# Challenge resolution precedure

## Context

I'm using Spec-Driven Development with a set of skills of my on making that help me build solutions the way I want, faster than if I was writing everything my self, but still keeping the AI in check, so it doesn't runs wild.

My first skill, helps me build a constitution, to make sure my agents have a set of ogligations according to the project's context. 

My second skills, helps me build my project structure, that could change overtime

After seting up my project structure, I usually start creating basic ADRs with important desitions I want to keep and document. Some of them are very simple. Others could be more complex and could need me to write specifications so that I can plan a big chunk of work. I mix agentic development with manual development depending on the size of the task.

## Development jounal

For more details, you can read my commit messages, I think they are clear enough to understand my reasoning. Here I will comment about some important changes or things that are not commiting changes.

I removed the .ipynb to work only with Quarto Markdown (qmd). That improved reproducibility, flexibility and data protection (among other qualities).

I removed the requierements.txt files, because we will use uv for managing environments. IMO is much better because of speed, information, easy to split dev versus prod, etc.

I fixed some dependency problems and I defined an explicit python version for this project, with a `.python-version` file.

I fixed some typos, and outdated syntax in the qmd. After that, I was able to run the qmd from end to end. I changes some formatting options to make it use a dark theme.

I read the full qmd report (rendered to html), to understand the current status and what the DS found out.