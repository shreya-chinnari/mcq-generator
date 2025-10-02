import os
import json
import traceback
import PyPDF2


def read_file(file):
    """
    Reads a file (PDF or TXT) and extracts text content.
    
    Args:
        file: File object uploaded or opened.
        
    Returns:
        str: Extracted text from the file.
        
    Raises:
        Exception: If file format is unsupported or reading fails.
    """
    try:
        # ✅ Check if the file is a PDF
        if file.name.endswith(".pdf"):
            text = ""  # initialize storage for extracted text
            pdf_reader = PyPDF2.PdfReader(file)  # create PDF reader object
            
            # ✅ Iterate over each page and extract text
            for page in pdf_reader.pages:
                page_text = page.extract_text()  # extract page text
                if page_text:  # ignore blank pages
                    text += page_text  # append extracted text
            return text

        # ✅ Handle text file (.txt)
        elif file.name.endswith(".txt"):
            return file.read().decode("utf-8")  # read and decode raw bytes to string

        # ❌ Unsupported file formats
        else:
            raise Exception("❌ Unsupported file format. Only PDF and TXT files are supported.")
    
    except Exception as e:
        # ⚠️ Log traceback for debugging in case of failure
        traceback.print_exception(type(e), e, e.__traceback__)
        # Re-raise a user-friendly error message
        raise Exception(f"⚠️ Error while reading the file: {str(e)}")


def get_table_data(quiz_str):
    """
    Converts quiz JSON string into a structured table-friendly list of dicts.
    
    Args:
        quiz_str (str): JSON string with quiz data.
        
    Returns:
        list[dict]: List containing quiz questions, options, and correct answers.
    """
    try:
        # ✅ Parse JSON string into Python dictionary
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []  # container for table rows

        # ✅ Loop through each quiz entry (key = Q1, Q2..., value = data)
        for key, value in quiz_dict.items():
            mcq = value.get("mcq", "")  # extract question text
            options_dict = value.get("options", {})  # extract options
            
            # ✅ Convert options dictionary into formatted string
            # Example: "A -> Option1 || B -> Option2"
            options = " || ".join(
                [f"{opt} -> {opt_val}" for opt, opt_val in options_dict.items()]
            )
            
            correct = value.get("correct", "")  # extract correct answer
            
            # ✅ Append structured row for table display
            quiz_table_data.append({
                "MCQ": mcq,
                "Choices": options,
                "Correct": correct
            })

        return quiz_table_data

    except Exception as e:
        # ⚠️ Log traceback if parsing fails
        traceback.print_exception(type(e), e, e.__traceback__)
        return False  # return False to indicate failure
