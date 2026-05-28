import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post

# Options
length_options = ["Short", "Medium", "Long"]

language_options = ["English", "Hinglish"]


def main():

    st.title("LinkedIn Post Generator")

    st.subheader("Codebasics Project")

    try:

        st.write("Loading tags...")

        fs = FewShotPosts()

        tags = fs.get_tags()

        st.write("Tags loaded successfully")

    except Exception as e:

        st.error(f"Backend Error: {e}")

        tags = ["General"]

    col1, col2, col3 = st.columns(3)

    with col1:

        selected_tag = st.selectbox(
            "Topic",
            options=tags
        )

    with col2:

        selected_length = st.selectbox(
            "Length",
            options=length_options
        )

    with col3:

        selected_language = st.selectbox(
            "Language",
            options=language_options
        )

    if st.button("Generate"):

        with st.spinner("Generating post..."):

            try:

                post = generate_post(
                    selected_length,
                    selected_language,
                    selected_tag
                )

                st.markdown("---")

                st.write(post)

            except Exception as e:

                st.error(f"Generation Error: {e}")


if __name__ == "__main__":
    main()