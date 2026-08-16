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

I chose the model we would use. The reasoning is below.

So far, I was working on the dev branch, because I was doing a bunch of small very simple changes. There was no need for a feature branch. I did one merge to main with a tag when the qmd was working, in case a broke it, so I knew where to roll back to recover the functionality. But now that I already understood the whole DS procees and the question the DS sent me, and I replied to them, it's time to roll up my sleeves. I'm making a plan to modularice the code, so it's maintainable in the future, bugs can be isolated so certain components, complexity is hidden behind functions, and many more advantages of modularizing.

I created `feat/modularization` branch and used my SDD skills to create an ADR about modularity, create specs, design, tasks and implement the tasks. Then I reviewed the work before sending a PR to dev. This is the first PR I send, since this is a very simple repo, but this is the biggest chunck of work so far and it could be useful to store the PR for somebody else to check in the future. I will still auto approve and merge my PR, because I'm all alone xD

I had to debug some problems with testing libraries, wrong paths that I changed to relative paths to the project's root, data leakage problem in test script, and more.

I generated a `model.py` script using my specs, then I reviewed it and fixed some mistakes. For example, the AI tryied to replace columns by 0, but I changed that to raising an error if any column we need was not found. 

I created a main section for the model.py script to test the end-to-end pipeline quickly and with debug tool. That's easier to debug IMO thather than using a test. The test is great for automatics alerts, but having a place to easily debug is very useful. This is not what I would do in general, I like other ways to debug. But there is not much time for that now. We can talk more about that duringthe technical interview.

When implementing the model training, I used the method's option to balance the data, so we can hidde complexity there and use tools already available to us instead of calculating it ourselfs.

I fixed some warnings for possible problems with data types on the test.

I cleaned up some files to create version 0.0.2

I implemented a first API skeleton with SDD. I checked the whole ADR, spec and code. I don't work much with FastAPI, so I made sure to understand every detail to learn and make sure everything made sense. At first, we only use a dummy model to test the structure is working.

After a couple iterations between SSD, reading each change, exploring with my debugger, and tweaking some details manually, I manages to have a working API with the real model being loaded from a pkl file from my file system. 

Then, I checked the predictions distribution, to make sure the model was not returning some dummy values.

That's enough for a localhost version. We can now start deploying this API to CGP

Then, I worked on deploying to GCP. I created an account with my personal e-mail, I set up a new project with billing activated. I asked an agent to generate templates to easily connect to my project and deploy. I had to debug a couple details. After a while, I managed to build a docker image locally and push it to Google Cloud Run. I ran the stress test, and after solving a couple dependency problems, it worked.

## Model choice

Depending on the business objective, it could be more important to identify as many positives as posible (delayed flights), or it could be more important to make sure our positive predictions are correct. My guess is that for this case, we care more about the first case, that means, we need a high recall. Depending on how much important is to minimize false negatives versus false positives, I would chose which F-Beta score to add to the table. Maybe F-2 or F-3 score could be good.

### GXBoost

This model is useless. Predicts every flight as not being delayed. It doesn't matter what metricts it has, it's not applicable to making decisions.

We could probably improve it, by better filtering the variables we give it and giving it more variables other than the 3 original cathegorical variables. But I won't improve it to optimize my time on this challenge. We can discuss this later during the tachnical interview, if you want.

We could also balance our classes, but that's what the DS did later.

### Logistic Regression

In our case recall for 1s is 0.03, so it's better than 0, but it's still terrible.

### XGBoost with Feature Importance and with Balance

Now we are talking.

Our recall for class 1 is 0.69. That's not good, but at least it's not trash xD we moved in a good direction.

### XGBoost with Feature Importance but without Balance

Without balance, this model is comparable with the original logistic regression. It's terrible. We are not using this model.

### Logistic Regression with Feature Importante and with Balance

Again, a decent model, thanks to the class balance. 0.69 recall for class 1 again. XGBoost is sliiiiiiightly better.

### Logistic Regression with Feature Importante but without Balance

Again, without balance, we get useless models. This is a very unbalance case. And thanks for that, because if it wasn't, we would be without a job with a pile of angry customers asking for refunds xD

### Final choice

"XGBoost with Feature Importance and with Balance" and "Logistic Regression with Feature Importante and with Balance" a very comparable.

If we HAVE to choose between those two without any more improvements, **I would choose logistic regression** because of prediction speed and simplicity and interpretability, specially if we need to run this model live or on edge. 

If we need to run it as a batch process, it wouldn't matter that much. Logitic regression is easier to interpret, but we can always use model agnostic tools to interpret model results globally and locally, like with Shapley Values, by using SHAP (SHapley Additive exPlanations), for example.

In the future, we we implemente continuous training, I would use both aproaches and chose the best in an automatic way. I would define a minimum improvement on a specific metric to use a more complex model than the currect champion. I would train multiple models later, because the flight's behaviour could change after a couple months or years, so the best model could change in the future.

## Possible improvements in DS development practices

- The DS hardcoded the top 10 features. That's bad because the logic is not reproducible with different datasets, so it would corrupt our results for future training in our continous training process.
- Using Jupyter Notebook is a bad practice, because it stores a bunch of metadata that could be accidentally commited, it's not Git friends, and so many other problems. I could talk about this for an hour (I gave a talk about this a couple years ago). It's better to use Quarto Notebooks or just use .py, .r, .sh, and other scripts.
- We could improve our feature engineering process. It was too generic and quick.
- I don't like these notebooks with bad models and incomplete preprocessing. The DS should look into that and present their final pipeline, without the history of his research, If we want to check his reasoning, we can check his commits or maybe another report that is tagged as containing obsolete results that were archived. I redid most of the analysis again, concluding that we had some useless models, and that not a good use of a teammate's time. 
- I found a big conceptual problem in the test script. We were leaking data by training with the whole dataset and then using a subset to validate. In that case, it's better to use the whole dataset to get the training report, or to use a completly different dataset to simulate a test report. But not a mix.
- We could condence all important variables in a set of config files. A global config, and three other configs with the differences between dev, stage and prod.

