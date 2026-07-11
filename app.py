import streamlit as st
import pandas as pd

# Configure the page
st.set_page_config(
    page_title="Bhagavad Gita Shlokas",
    layout="wide"
)


# Load the dataset
df = pd.read_excel(
    "bhagavad-gita.xlsx",
    sheet_name="Bhagavad-Gita",
    engine="openpyxl"
)

# Store favourite verses
if "favourites" not in st.session_state:
    st.session_state.favourites = []

# Main Heading
# Main Hero Section
st.markdown("""
<div style="
text-align:center;
padding:40px;
background:linear-gradient(135deg,#1E3A8A,#312E81);
border-radius:25px;
margin-bottom:30px;
box-shadow:0 0 25px rgba(0,0,0,.35);
">

<h1 style="
font-size:55px;
color:white;
margin-bottom:10px;
">
📖 Bhagavad Gita
</h1>

<p style="
font-size:24px;
color:#E5E7EB;
">
The Eternal Wisdom for Everyday Life
</p>

</div>
""", unsafe_allow_html=True)

# Sidebar

st.sidebar.markdown("""
<div style="
text-align:center;
padding:20px;
border-radius:15px;
background:linear-gradient(135deg,#1E3A8A,#312E81);
margin-bottom:15px;
">

<h2 style="color:white;">
📖 Bhagavad Gita
</h2>

<p style="color:#E5E7EB;">
Explore Divine Wisdom
</p>

</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🧭 Navigation")

page = st.sidebar.selectbox(
    "Choose a Section",
    [
        "🏠 Home",
        "📚 Browse Shlokas",
        "🔍 Search",
        "❤️ Favourites",
        "ℹ️ About"
    ]
)

st.sidebar.info(f"📍 Current Page\n\n**{page}**")
st.sidebar.divider()

st.sidebar.markdown("### 📊 App Statistics")

st.sidebar.metric("📖 Chapters", df["Chapter"].nunique())

st.sidebar.metric("📝 Shlokas", len(df))

st.sidebar.metric("❤️ Favourites", len(st.session_state.favourites))

st.sidebar.divider()

st.sidebar.markdown("### 💻 Built With")

st.sidebar.markdown("""
- 🐍 Python
- 🎈 Streamlit
- 📊 Pandas
- 📄 Excel Dataset
""")

st.sidebar.divider()

st.sidebar.caption("🙏 May Lord Krishna guide your path.")
st.sidebar.caption("🌸 May the teachings of the Gita inspire you.")
st.sidebar.caption("Version 1.0")

# Page Navigation
# Home page:
if page == "🏠 Home":

    st.header("🏠 Home")
    st.write("Explore the timeless wisdom of the Bhagavad Gita.")

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📖 Chapters", df["Chapter"].nunique())

    with col2:
        st.metric("📝 Total Shlokas", len(df))

    with col3:
        st.metric("🌍 Languages", 3)

    st.divider()

    st.subheader("🌟 Daily Inspiration")

    if st.button("🎲 Inspire Me"):
        st.session_state.random_verse = df.sample(1).iloc[0]

    if "random_verse" not in st.session_state:
        st.session_state.random_verse = df.sample(1).iloc[0]

    featured = st.session_state.random_verse

    st.write(f"### 📖 {featured['Title']}")
    st.write(f"**Chapter:** {featured['Chapter']}")
    st.write(f"**Verse:** {featured['Verse']}")

    st.subheader("🕉️ Sanskrit Shloka")
    st.info(featured["Sanskrit Anuvad"])

    st.subheader("🪔 Hindi Translation")
    st.success(featured["Hindi Anuvad"])

    st.subheader("🌍 English Translation")
    st.warning(featured["English Translation"])

elif page == "📚 Browse Shlokas":
    st.header("📚 Browse Shlokas")
    st.write("Select a chapter to explore its verses.")

    # Get all unique chapters
    chapters = sorted(
        df["Chapter"].unique(),
        key=lambda x: int(str(x).replace("Chapter ", ""))
)

    # Chapter Dropdown
    selected_chapter = st.selectbox(
        "📖 Select Chapter",
        chapters
    )

    # Filter data based on selected chapter
    chapter_data = df[df["Chapter"] == selected_chapter]
    # Get all verses of the selected chapter
    verses = chapter_data["Verse"].unique()

    # Verse Dropdown
    selected_verse = st.selectbox(
    "📝 Select Verse",
    verses
)
    # Get the selected verse details
    verse_data = chapter_data[chapter_data["Verse"] == selected_verse].iloc[0]
    st.divider()

    st.subheader("📖 Adhyay")
    st.write(verse_data["Title"])
    st.subheader("🕉️ Sanskrit Shloka")
    st.info(verse_data["Sanskrit Anuvad"])
    st.subheader("🪔 Hindi Translation")
    st.success(verse_data["Hindi Anuvad"])
    st.subheader("🌍 English Translation")
    st.warning(verse_data["English Translation"])

    # Create a unique ID for the verse
    verse_id = f"{verse_data['Chapter']}-{verse_data['Verse']}"

# Add to Favourites button
    if st.button("⭐ Add to Favourites"):
        
        if verse_id not in [item["id"] for item in st.session_state.favourites]:

            st.session_state.favourites.append({
            "id": verse_id,
            "Title": verse_data["Title"],
            "Chapter": verse_data["Chapter"],
            "Verse": verse_data["Verse"],
            "Sanskrit": verse_data["Sanskrit Anuvad"],
            "Hindi": verse_data["Hindi Anuvad"],
            "English": verse_data["English Translation"]
        })

        st.success("⭐ Verse added to Favourites!")

    else:
        st.info("⭐ This verse is already in your Favourites.")


    
elif page == "🔍 Search":

    st.header("🔍 Search Bhagavad Gita")

    st.write("Search Bhagavad Gita by language or across all translations.")

    search_by = st.selectbox(
        "🔍 Search By",
        [
            "All",
            "Sanskrit",
            "Hindi",
            "English"
        ]
    )

    search_query = st.text_input(
        "🔎 Enter a keyword",
        placeholder="Example: karma, soul, yoga"
    )

    # Search only if the user enters something
    if search_query:

        keyword = search_query.lower()

        if search_by == "All":
            results = df[
                df.astype(str)
                  .apply(lambda x: x.str.lower())
                  .apply(lambda x: x.str.contains(keyword))
                  .any(axis=1)
            ]

        elif search_by == "Sanskrit":
            results = df[
                df["Sanskrit Anuvad"].str.lower().str.contains(keyword)
            ]

        elif search_by == "Hindi":
            results = df[
                df["Hindi Anuvad"].str.lower().str.contains(keyword)
            ]

        elif search_by == "English":
            results = df[
                df["English Translation"].str.lower().str.contains(keyword)
            ]

        if results.empty:
            st.error("❌ No matching shlokas found.")

        else:
            st.success(
                f"✅ Found {len(results)} matching result(s). Showing first {min(len(results),10)}."
            )

            for _, row in results.head(10).iterrows():

                st.divider()

                st.subheader(f"📖 {row['Title']}")
                st.write(f"**Chapter:** {row['Chapter']}")
                st.write(f"**Verse:** {row['Verse']}")

                st.subheader("🕉️ Sanskrit Shloka")
                st.info(row["Sanskrit Anuvad"])

                st.subheader("🪔 Hindi Translation")
                st.success(row["Hindi Anuvad"])

                st.subheader("🌍 English Translation")
                st.warning(row["English Translation"])

# Favourites page:
elif page == "❤️ Favourites":

    st.header("❤️ Favourite Shlokas")

    if len(st.session_state.favourites) == 0:
        st.info("No favourite verses added yet.")

    else:

        st.success(f"You have {len(st.session_state.favourites)} favourite verse(s).")

        for i, fav in enumerate(st.session_state.favourites):
            if st.button(
                "🗑️ Remove from Favourites",
                key=f"remove_{fav['id']}"
                ):
                st.session_state.favourites.remove(fav)
                st.rerun()

            st.divider()

            st.subheader(f"📖 {fav['Title']}")

            st.write(f"**Chapter:** {fav['Chapter']}")
            st.write(f"**Verse:** {fav['Verse']}")

            st.subheader("🕉️ Sanskrit Shloka")
            st.info(fav["Sanskrit"])

            st.subheader("🪔 Hindi Translation")
            st.success(fav["Hindi"])

            st.subheader("🌍 English Translation")
            st.warning(fav["English"])
            if st.button("❌ Remove from Favourites", key=f"remove_{i}"):
                st.session_state.favourites.pop(i)
                st.rerun()

# about page: 
elif page == "ℹ️ About":

    st.header("ℹ️ About This Project")

    st.write(
        """
This application allows users to explore the sacred teachings of the Bhagavad Gita
through an interactive and user-friendly interface.
"""
    )

    st.divider()

    st.subheader("✨ Features")

    st.markdown("""
- 📖 Browse all 18 chapters
- 📝 Read Sanskrit Shlokas
- 🪔 Hindi Translation
- 🌍 English Translation
- 🔍 Powerful Search
- ⭐ Featured Verse on Home Page
""")

    st.divider()

    st.subheader("🛠️ Technologies Used")

    st.markdown("""
- 🐍 Python
- 🎈 Streamlit
- 📊 Pandas
- 📄 Excel Dataset
""")

    st.divider()

    st.subheader("👨‍💻 Developer")

    st.info("""
**Kartik**

B.Tech CSE Student  
Punjabi University, Patiala
""")

    st.caption("Version 1.0 • Made with ❤️ using Streamlit")