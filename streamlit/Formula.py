import streamlit as st

#title - used for title
st.title("Welcome to Tops technologies")

#Header
st.header("Data Science")

#subheader
st.subheader("Streamlit")

#information
st.info("It showing information of students")

#warning
st.warning("please attend your lecture")

#write
st.write("Student name")
st.write(range(50))

#Error
st.error("data not founded")

#success
st.success("You have done")

#markdown
st.markdown("# Hello students")
st.markdown("## Hello students")
st.markdown("### Hello students")
st.markdown(":moon:")

#text
st.text("Tops technoligies student")

#caption
st.caption("Its your caption")

#mathematical expression
st.latex(r''' a x^2 + b x + c''')

#image
#st.image(path)

#widget

#checkbox
st.checkbox('login')

#button
st.button("Click")

#radio widget
st.radio("gender", ["Male", "Female", "other"])

#select box
st.selectbox("Course", ["Python", "cloud", "Java"])

#multi select
st.multiselect("Department", ["faculty", "sales", "marketing"])

#select slider
st.select_slider("Rating", ["Average", "Good", "Bad"])

#slider
st.slider("Enter a number", 0, 100)

#number input
st.number_input("Pick a numbe", 0, 100)

#text input
st.text_input("Email address")

#date input
st.date_input("Date")

#time input
st.time_input("what is the time")

#text area
st.text_area("Feedback")

#upload file
st.file_uploader("upload our file")

#color
st.color_picker("color")

st.progress(90)

st.spinner("just wait")

st.balloons()

#sidebar
st.sidebar.title("this is side bar")
st.sidebar.text_input("Mail adress")
st.sidebar.text_input("password")
st.sidebar.button("Submit")
st.sidebar.radio("Professional Expert", ["Student", "Working", "Others"])