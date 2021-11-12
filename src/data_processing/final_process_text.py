import re
import numpy as np
import pandas as pd
import string


def span_overlap(span1, span2):
    # check if two spans overlaps
    # -1 if the spans does not overlap
    # 0 if the largest span is the first one
    # 1 the largest span is the second one
    if span1[0] <= span2[1] and span2[0] <= span1[1]:
        span1_length = span1[1] - span1[0]
        span2_length = span2[1] - span2[0]
        if span1_length >= span2_length:
            overlap = 0
        else:
            overlap = 1
    else:
        overlap = -1

    return overlap

def find_all_sections_title_single_report(report, sections):
    # this function find the span of each section and returns a data frame with the following columns
    # section_name, start_title, end_title, start_section, end_section

    ###########
    # STEP 1: Find the sections titles and sort
    columns = ["section_name", "start_title", "end_title", "start_section", "end_section"]
    sections_found = find_titles_span_and_sort(columns, report, sections)

    #########
    # STEP 2. Check if any section title overlaps and delete the shortest title
    sections_found = remove_overlapping_sections(sections_found)

    #######
    # STEP 3: find the contents of each section.
    sections_found = find_sections_content(report, sections_found)

    return sections_found


def find_titles_span_and_sort(columns, report, sections):
    sections_found = pd.DataFrame(index=np.arange(0, len(sections)), columns=columns)
    # counter for the number of sections found. In this way the unused rows will be  discarded
    i = 0
    for section in sections:
        # find the occurrence of the section text inside the report
        section_title_span = get_text_span(section, report)
        # if the section is not found skip and go to the next
        if section_title_span[0] == -1:
            continue
        else:
            sections_found.iloc[i] = [section, section_title_span[0], section_title_span[1], 0, 0]
            i += 1

    # delete unused rows
    sections_found = sections_found[:i]
    # sort by start_title
    sections_found = sections_found.sort_values(by=columns[1])
    return sections_found


def remove_overlapping_sections(sections_found):
    # counter for the original variable
    i = 0
    # counter for the new temporal variable
    j = 0
    # a copy of the data frame is needed since the elements inside are going to be used to assign
    # other elements inside since the elements are copy by reference this produce a chain assigment
    # and slow significantly the performance
    columns = list(sections_found.columns.values)
    temp_sections_found = pd.DataFrame(index=np.arange(0, len(sections_found.index)), columns=columns)
    while i <= len(sections_found.index) - 2:
        # check for overlap of section i with section i+1
        overlap = span_overlap(sections_found.iloc[i, [1, 2]], sections_found.iloc[i + 1, [1, 2]])

        if overlap == 0:
            temp_sections_found.iloc[j] = sections_found.iloc[i]
            # jump one to not evaluate the same section again
            i += 1
            j += 1
        elif overlap == 1:
            temp_sections_found.iloc[j] = sections_found.iloc[i + 1]
            # jump one to not evaluate the same section again
            i += 1
            j += 1
        else:
            temp_sections_found.iloc[j] = sections_found.iloc[i]
            j += 1
        i += 1

    # delete unused rows
    temp_sections_found.iloc[j] = sections_found.iloc[i]
    sections_found = temp_sections_found[:j + 1]

    return sections_found



def find_sections_content(report, sections_found):
    # This step is important because some sections are empty given that the next section
    # starts right away at the end of the other
    temp_sections_found = sections_found.copy()
    for i in range(len(sections_found.index) - 1):
        sec1_end = temp_sections_found.loc[i, "end_title"]
        sec2_start = temp_sections_found.loc[i + 1, "start_title"]

        if sec1_end == sec2_start:
            # if the section is empty simply put the end of the section as start and finish of the section
            sections_found.iloc[i, [3, 4]] = [sec1_end, sec1_end]
        else:
            sections_found.iloc[i, [3, 4]] = [sec1_end, sec2_start]

    # for the last section is up to the length of the report - 1
    i = len(sections_found.index) - 1
    sec1_end = temp_sections_found.loc[i, "end_title"]
    sections_found.iloc[i, [3, 4]] = [sec1_end, len(report)]

    return sections_found



def extract_section_contents_single_report(report, sections_found, sections_list=None, new_line=True,
                                           delete_empty_sections=True):
    # this function delete all the sections titles found in an
    # attempt to clean the text an reduce the false positives
    # if new_line is equal to true the sections are appended using a new line character
    # if new)line is false the sections are appended using a space
    # Sections_list: is a list with the specific sections to remove, by default None

    # iterate over all the found sections in the given report
    report_cleaned = []

    if sections_list is None:
        for i in range(len(sections_found.index)):
            span_section = sections_found.loc[i, ["start_section", "end_section"]]
            if (span_section[1] == span_section[0]) and delete_empty_sections:
                continue
            else:
                report_cleaned.append(report[span_section[0]:span_section[1]])
    else:
        indices = sections_found['section_name'].isin(sections_list)
        span_sections = sections_found.loc[indices, ["start_section", "end_section"]]
        for i in range(span_sections.shape[0]):
            if (span_sections.iloc[i, 0] == span_sections.iloc[i, 1]) and delete_empty_sections:
                continue
            else:
                report_cleaned.append(report[span_sections.iloc[i, 0]:span_sections.iloc[i, 1]])

    if new_line:
        report = "\n".join(report_cleaned)
    else:
        report = " ".join(report_cleaned)

    return report



def get_text_span(subtext, text):
    # get the span of a given subtext inside a text
    # if the subtext if not inside both start and end is -1

    start_span = text.find(subtext)

    if start_span == -1:
        end_span = -1
    else:
        end_span = start_span + len(subtext)

    span = [start_span, end_span]

    return span


def extract(x, sections, takeLastInstance = False):
    if takeLastInstance:
        import re
        instances = [i.start() for i in re.finditer("Assessment", x)]
        if len(instances) > 1:
            lastInstance = max(instances)
            x = x[lastInstance:]
    sections_found = find_all_sections_title_single_report(x, sections)
    extracted = extract_section_contents_single_report(x, sections_found, sections_list=sections, new_line=True,
                                               delete_empty_sections=True)
    return sections_found, extracted

def sectionize(report):
    if report.find('Plan and Assessment') != -1:
        reportExtract = extract(report, sections=['Plan and Assessment'])
    elif report.find('Assessment and Plan') != -1:
        reportExtract = extract(report, sections=['Assessment and Plan'])
    elif report.find('Assessment') != -1:
        reportExtract = extract(report, sections=['Assessment'], takeLastInstance=True)
    else:
        reportExtractDF = pd.DataFrame({'section_name': ['NULL'],
                                        'start_title':[-99],
                                        'end_title': [-99],
                                        'start_section': [-99],
                                        'end_section': [-99]})
        reportExtract = [reportExtractDF, report]
    return reportExtract

def clean_text(note_text: str):
    """
      This function performs basic cleaning for Stanford clinical text
    """

    note_text = re.sub(r"\s(\?|¿)\s", ' ', note_text)
    note_text = re.sub(r"\n", ' ', note_text)
    note_text = re.sub(r"(\?|\¿)", ' ', note_text)
    note_text = re.sub(u"\xa0", ' ', note_text)
    # remove double spaces
    note_text = re.sub(r"\s{2,}", ' ', note_text)

    #Remove plan
    # note_text = re.sub(r"(?i)\w*:", '', note_text) # Remove Section headers
    note_text = re.sub(r"\d{1,2}/\d{2}/\d{4}", '', note_text)
    note_text = re.sub(r"\d{1,2}/\d{2}/\d{2}", '', note_text)


    note_text = re.sub(r"\d", '', note_text) #Remove digits
    note_text = re.sub(r"\[\W*\]", ' ', note_text)
    note_text = re.sub(r"\(\W*\)", ' ', note_text)
    note_text = re.sub(r"[\(\)\[\]]", '', note_text)
    note_text = re.sub(r"\/", " ", note_text)
    note_text = re.sub(r"[^\w\s\.]", '  ', note_text)
    note_text = re.sub(r"\s{2,}", ' ', note_text)

    note_text = re.sub("\s(?=\.)", '', note_text)

    note_text = note_text.lower()
    return note_text
