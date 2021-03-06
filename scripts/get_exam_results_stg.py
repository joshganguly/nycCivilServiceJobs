import sys, os, django

sys.path.append("../nycCivilServiceJobs")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nycCivilServiceJobs.settings")
django.setup()

import pandas as pd
from sodapy import Socrata
from examresults.models import ExamResultsActive
from examresults.models import ExamResultsTerminated
from django.utils import timezone
import datetime

# Fetch Active Exam Results from NYC Open Data

client = Socrata(
    "data.cityofnewyork.us",
    "m7QHRP2U6tqRR7XCge8TzIRUW",
    username="nycCivilService.csgy6063@gmail.com",
    password="team4Pythonpir@tes",
    timeout=30,
)

# Fetch Terminated Exam Results from NYC Open Data


def save_exam_result_active():
    ExamResultsActive.objects.all().delete()
    print("Deleted Previous Entries in ExamResultsActive")

    columns = [
        "exam_no",
        "list_no",
        "first_name",
        "last_name",
        "adj_fa",
        "list_title_code",
        "list_title_desc",
        "group_no",
        "list_agency_code",
        "list_agency_desc",
        "established_date",
        "anniversary_date",
        "mi",
        "published_date",
        "veteran_credit",
        "extension_date",
        "sibling_lgy_credit",
        "list_div_code",
        "parent_lgy_credit",
        "residency_credit",
    ]

    exam_no = client.get("vx8i-nprf", select="distinct exam_no")
    exam_no_df = pd.DataFrame.from_records(exam_no)
    limit_per_exam = 8
    total_entries = 0
    exam_count = 0
    total_exams = len(exam_no_df.index)
    while exam_count < total_exams:
        for index, row in exam_no_df.iterrows():
            s = "exam_no='" + (row["exam_no"]) + "' AND 'first_name' is not null"
            try:
                exam_result_list = client.get(
                    "vx8i-nprf", where=s, limit=limit_per_exam
                )
            except Exception as e:
                print("API Errors", e)
            else:
                exam_result_list_df = pd.DataFrame.from_records(exam_result_list)
                exam_result_list_df = exam_result_list_df.replace(
                    r"^\s*$", None, regex=True
                )
                exam_result_list_df = exam_result_list_df.where(
                    exam_result_list_df.notnull(), None
                )
                exam_result_list_df = exam_result_list_df[
                    exam_result_list_df["first_name"].notnull()
                    & exam_result_list_df["last_name"].notnull()
                ]

                for c in columns:
                    if c not in exam_result_list_df.columns:
                        exam_result_list_df[c] = None

                entries = []
                for index, row in exam_result_list_df.iterrows():
                    if len(entries) < limit_per_exam:
                        try:
                            entries.append(
                                ExamResultsActive(
                                    exam_number=row["exam_no"],
                                    display_exam_number=row["exam_no"],
                                    list_number=row["list_no"],
                                    first_name=row["first_name"],
                                    last_name=row["last_name"],
                                    middle_initial=row["mi"],
                                    adjust_final_average=row["adj_fa"],
                                    list_title_code=row["list_title_code"],
                                    list_title_desc=row["list_title_desc"],
                                    group_number=row["group_no"],
                                    list_agency_code_promo=row["list_agency_code"],
                                    list_agency_code_promo_desc=row["list_agency_desc"],
                                    list_div_code_promo=row["list_div_code"],
                                    anniversary_date=getAwareDate(
                                        row["anniversary_date"]
                                    ),
                                    published_date=getAwareDate(row["published_date"]),
                                    established_date=getAwareDate(
                                        row["established_date"]
                                    ),
                                    extension_date=getAwareDate(row["extension_date"]),
                                    veteran_credit=row["veteran_credit"],
                                    parent_legacy_credit=row["parent_lgy_credit"],
                                    sibling_legacy_credit=row["sibling_lgy_credit"],
                                    residency_credit=row["residency_credit"],
                                )
                            )
                        except Exception as e:
                            print("Error", e)
                total_entries += len(entries)
                exam_count += 1
                ExamResultsActive.objects.bulk_create(entries, ignore_conflicts=True)

    print("Total Objects expected in ExamResultActive: ", total_entries)
    print(
        "Total Objects added in ExamResultActive: ", ExamResultsActive.objects.count()
    )


def save_exam_result_terminated():

    try:
        record_count = client.get("qu8g-sxqf", select="COUNT(*)")[0]["COUNT"]
        exam_result_list = client.get(
            "qu8g-sxqf",
            select="distinct exam_no,list_title_code,list_title_desc",
            limit=record_count,
        )
    except Exception as e:
        print("Client Error", e)
    else:
        ExamResultsTerminated.objects.all().delete()
        print("\nDeleted Previous Entries in ExamResultsTerminated")
        exam_result_list_df = pd.DataFrame.from_records(exam_result_list)
        exam_result_list_df = exam_result_list_df.where(
            exam_result_list_df.notnull(), None
        )

        columns = ["exam_no", "list_title_code", "list_title_desc"]
        for c in columns:
            if c not in exam_result_list_df.columns:
                exam_result_list_df[c] = None
        entries = []

        for index, row in exam_result_list_df.iterrows():
            try:

                entries.append(
                    ExamResultsTerminated(
                        exam_number=row["exam_no"],
                        list_title_code=row["list_title_code"],
                        list_title_desc=row["list_title_desc"],
                    )
                )
            except Exception as e:
                print("Error", e)
        ExamResultsTerminated.objects.bulk_create(entries, ignore_conflicts=True)
        print("Total Objects expected in ExamResultTerminated: ", len(entries))
        print(
            "Total Objects added in ExamResultTerminated: ",
            ExamResultsTerminated.objects.count(),
        )


def getAwareDate(inputDate):
    if not inputDate:
        return
    tz = timezone.get_default_timezone()
    aware_datetime = datetime.datetime.fromisoformat(inputDate)
    date_aware = aware_datetime.replace(tzinfo=tz)
    return date_aware


def convertDateFormat(inputDate):
    if not inputDate:
        return None
    return datetime.datetime.strptime(inputDate, "%d-%b-%Y").strftime("%Y-%m-%d")


if __name__ == "__main__":
    save_exam_result_active()
    save_exam_result_terminated()
