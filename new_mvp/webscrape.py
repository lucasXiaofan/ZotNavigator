# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# # from webdriver_manager.firefox.servi
# from webdriver_manager.microsoft import EdgeChromiumDriverManager
# import webbrowser

# def open_google_with_browser():
#     try:
#         # Try using Chrome
#         driver = webdriver.Chrome(ChromeDriverManager().install())
#     except:
#         # try:
#         #     # If Chrome is not available, try using Firefox
#         #     driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
#         # except:
#         try:
#             # If Firefox is not available, try using Edge
#             driver = webdriver.Edge(EdgeChromiumDriverManager().install())
#         except Exception as e:
#             # If none of the browsers are available, print an error message
#             print("No supported browser found or WebDriver issue encountered.")
#             print("Error:", e)
#             return

#     # Open Google
#     driver.get("https://www.google.com")

#     # You can add a delay here if you want to keep the browser open for a while
#     # import time
#     # time.sleep(10)

#     # Close the browser
#     driver.quit()

# if __name__ == "__main__":
#     open_google_with_browser()
