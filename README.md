# University API &middot; ![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/SoftwyRD/university-api/checks.yml?label=Checks)
University API is a simple API that lets INTEC's students plan their next selection in an easier and simpler way.

## The Problem
With every new trimester coming, students have to plan which subjects they are going to take. This should be an easy task, but subject sections interfere between them from subject to subject. This means that you may have 2 important subjects to take, but must choose 1. This leads to some questions:
- Which one is more important?
- Can I change the section so I can take both?
- Will I be available to take the subject in that schedule?

This kind of questions are normal and are not a problem themselves, but when we are in selection process, we are in live. This means that every minute you spend thinking and planning, each section is taking students, creating the possibility of being out due to the student limit per section.

## The Solution
To avoid having to take action in live, we can use this API to plan our next selection. This API will let you know which subjects you can take, which ones you can't, and which ones you can take if you change the section. This way, you can plan your selection in advance and take action in live only when you are sure of what you are doing.

## How to use it
This API is available at https://api.unimate.softwy.com/api/docs/. The

## Disclaimer
This API is not affiliated with INTEC. The data used in this API is obtained from the INTEC website, and is not guaranteed to be accurate. This API is provided as is, and the author is not responsible for any damage caused by using this API.

## How to run it
This API is built using [DRF](https://www.django-rest-framework.org/), and uses [Django](https://www.djangoproject.com/) as the backend. To run it, you need to have [Python](https://www.python.org/) installed. Then, you can install the dependencies using `pip install -r requirements.txt`. After that, you can run the API using `python manage.py runserver`.

## Frontend
This API is used by the [University App](https://github.com/SoftwyRD/university-app), which is a React app that uses this API to provide a better user experience.

## Languages
This API is available in English, but Spanish support is coming soon.
