# import streamlit as st
# from streamlit_webrtc import webrtc_streamer
# import av
# import cv2
# import numpy as np
# import mediapipe as mp
# from keras.models import load_model
# import webbrowser
#
# model = load_model("model.h5")
# label = np.load("labels.npy")
# holistic = mp.solutions.holistic
# hands = mp.solutions.hands
# holis = holistic.Holistic()
# drawing = mp.solutions.drawing_utils
#
#
# # @st.cache(suppress_st_warning=True)
# # def load_resources():
# #     model = load_model("model.h5")
# #     label = np.load("labels.npy")
# #     holistic = mp.solutions.holistic
# #     hands = mp.solutions.hands
# #     holis = holistic.Holistic()
# #     drawing = mp.solutions.drawing_utils
# #     return model, label, holis, hands, drawing
# #
# #
# # # Initialize resources
# # model, label, holis, hands, drawing = load_resources()
#
# st.header("Emotion Based Books Recommender")
#
# if "run" not in st.session_state:
#     st.session_state["run"] = "true"
#
# try:
#     emotion = np.load("emotion.npy")[0]
# except:
#     emotion = ""
#
# if not (emotion):
#     st.session_state["run"] = "true"
# else:
#     st.session_state["run"] = "false"
#
#
# class EmotionProcessor:
#     def recv(self, frame):
#         frm = frame.to_ndarray(format="bgr24")
#
#         ##############################
#         frm = cv2.flip(frm, 1)
#
#         res = holis.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
#
#         lst = []
#
#         if res.face_landmarks:
#             for i in res.face_landmarks.landmark:
#                 lst.append(i.x - res.face_landmarks.landmark[1].x)
#                 lst.append(i.y - res.face_landmarks.landmark[1].y)
#
#             if res.left_hand_landmarks:
#                 for i in res.left_hand_landmarks.landmark:
#                     lst.append(i.x - res.left_hand_landmarks.landmark[8].x)
#                     lst.append(i.y - res.left_hand_landmarks.landmark[8].y)
#             else:
#                 for i in range(42):
#                     lst.append(0.0)
#
#             if res.right_hand_landmarks:
#                 for i in res.right_hand_landmarks.landmark:
#                     lst.append(i.x - res.right_hand_landmarks.landmark[8].x)
#                     lst.append(i.y - res.right_hand_landmarks.landmark[8].y)
#             else:
#                 for i in range(42):
#                     lst.append(0.0)
#
#             lst = np.array(lst).reshape(1, -1)
#
#             pred = label[np.argmax(model.predict(lst))]
#
#             print(pred)
#             cv2.putText(frm, pred, (50, 50), cv2.FONT_ITALIC, 1, (255, 0, 0), 2)
#
#             np.save("emotion.npy", np.array([pred]))
#
#         drawing.draw_landmarks(frm, res.face_landmarks, mp.solutions.holistic.FACEMESH_TESSELATION,
#                                landmark_drawing_spec=drawing.DrawingSpec(color=(0, 0, 255), thickness=-1,
#                                                                          circle_radius=1),
#                                connection_drawing_spec=drawing.DrawingSpec(thickness=1))
#         drawing.draw_landmarks(frm, res.left_hand_landmarks, hands.HAND_CONNECTIONS)
#         drawing.draw_landmarks(frm, res.right_hand_landmarks, hands.HAND_CONNECTIONS)
#
#         ##############################
#
#         return av.VideoFrame.from_ndarray(frm, format="bgr24")
#
#
# lang = st.selectbox(
#    "Choose your preferred language",
#    ("Assamese", "Bengali", "Bodo", "Dogri", "Gujarati", "Hindi", "Kannada", "Kashmiri", "Konkani", "Maithili", "Malayalam", "Manipuri", "Marathi", "Nepali", "Odia (Oriya)", "Punjabi", "Sanskrit", "Santali", "Sindhi", "Tamil", "Telugu", "Urdu", "English"),
#    index=None,
#    placeholder="Language",
# )
# # singer = st.text_input("singer")
#
# if lang and st.session_state["run"] != "false":
# 	webrtc_streamer(key="key", desired_playing_state=True,
# 				video_processor_factory=EmotionProcessor)
#
# btn = st.button("Recommend me books")
#
# if btn:
#     if not (emotion):
#         st.warning("Please let me capture your emotion first")
#         st.session_state["run"] = "true"
#     else:
#         webbrowser.open( f"https://www.bookswagon.com/search-books/{lang}+{emotion}+book")
#         np.save("emotion.npy", np.array([""]))
#         st.session_state["run"] = "false"
import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import cv2
import numpy as np
import mediapipe as mp
from keras.models import load_model
import webbrowser

def main():
    model = load_model("model.h5")
    label = np.load("labels.npy")
    holistic = mp.solutions.holistic
    hands = mp.solutions.hands
    holis = holistic.Holistic()
    drawing = mp.solutions.drawing_utils

    st.header("Emotion Based Books Recommender")

    if "run" not in st.session_state:
        st.session_state["run"] = "true"

    try:
        emotion = np.load("emotion.npy")[0]
    except:
        emotion = ""

    if not emotion:
        st.session_state["run"] = "true"
    else:
        st.session_state["run"] = "false"

    class EmotionProcessor:
        def recv(self, frame):
            frm = frame.to_ndarray(format="bgr24")

            ##############################
            frm = cv2.flip(frm, 1)

            res = holis.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

            lst = []

            if res.face_landmarks:
                for i in res.face_landmarks.landmark:
                    lst.append(i.x - res.face_landmarks.landmark[1].x)
                    lst.append(i.y - res.face_landmarks.landmark[1].y)

                if res.left_hand_landmarks:
                    for i in res.left_hand_landmarks.landmark:
                        lst.append(i.x - res.left_hand_landmarks.landmark[8].x)
                        lst.append(i.y - res.left_hand_landmarks.landmark[8].y)
                else:
                    for i in range(42):
                        lst.append(0.0)

                if res.right_hand_landmarks:
                    for i in res.right_hand_landmarks.landmark:
                        lst.append(i.x - res.right_hand_landmarks.landmark[8].x)
                        lst.append(i.y - res.right_hand_landmarks.landmark[8].y)
                else:
                    for i in range(42):
                        lst.append(0.0)

                lst = np.array(lst).reshape(1, -1)

                pred = label[np.argmax(model.predict(lst))]

                print(pred)
                cv2.putText(frm, pred, (50, 50), cv2.FONT_ITALIC, 1, (255, 0, 0), 2)

                np.save("emotion.npy", np.array([pred]))

            drawing.draw_landmarks(frm, res.face_landmarks, mp.solutions.holistic.FACEMESH_TESSELATION,
                                   landmark_drawing_spec=drawing.DrawingSpec(color=(0, 0, 255), thickness=-1,
                                                                             circle_radius=1),
                                   connection_drawing_spec=drawing.DrawingSpec(thickness=1))
            drawing.draw_landmarks(frm, res.left_hand_landmarks, hands.HAND_CONNECTIONS)
            drawing.draw_landmarks(frm, res.right_hand_landmarks, hands.HAND_CONNECTIONS)

            ##############################

            return av.VideoFrame.from_ndarray(frm, format="bgr24")

    lang = st.selectbox(
       "Choose your preferred language",
       ("Assamese", "Bengali", "Bodo", "Dogri", "Gujarati", "Hindi", "Kannada", "Kashmiri", "Konkani", "Maithili", "Malayalam", "Manipuri", "Marathi", "Nepali", "Odia (Oriya)", "Punjabi", "Sanskrit", "Santali", "Sindhi", "Tamil", "Telugu", "Urdu", "English"),
       index=None,
       placeholder="Language",
    )

    if lang and st.session_state["run"] != "false":
        webrtc_streamer(key="key", desired_playing_state=True,
                        video_processor_factory=EmotionProcessor)

    btn = st.button("Recommend me books")

    if btn:
        if not emotion:
            st.warning("Please let me capture your emotion first")
            st.session_state["run"] = "true"
        else:
            webbrowser.open(f"https://www.bookswagon.com/search-books/{lang}+{emotion}+book")
            np.save("emotion.npy", np.array([""]))
            st.session_state["run"] = "false"

if __name__ == "__main__":
    main()