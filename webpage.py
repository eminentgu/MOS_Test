import gradio as gr

class MOSApp:
    MOS = {
        1: "1-Bad", 1.5: "1.5", 2: "2-Poor", 2.5: "2.5", 3: "3-Fair",
        3.5: "3.5", 4: "4-Good", 4.5: "4.5", 5: "5-Excellent"
    }

    def __init__(self):
        self.current_files = ['1.wav', '2.wav','3.wav','4.wav','5.wav']

    def initialize_state(self):
        return {
            "index": 0,
            "selected_MOS": [],
            "tester_id": "",
            "data_store": {}
        }

    def submit_options(self, overall_quality, issues_noticed, pitch_speed_fluency, emotional_expression, voice_pleasantness, state):
        if not state["tester_id"]:
            return None, "Please enter your tester ID first.", -1, None, -1, -1, -1, state

        if state["index"] < len(self.current_files) - 1:
            state["selected_MOS"].append((overall_quality, issues_noticed, pitch_speed_fluency, emotional_expression, voice_pleasantness))
            state["index"] += 1
            current_audio = self.current_files[state["index"]]
            return current_audio, f"#### you are rating {state['index']+1} out of {str(len(self.current_files))},after submitting Scroll UP to Step 2 to hear the new audio", -1, None, -1, -1, -1, state
        elif state["index"] == len(self.current_files) - 1:
            state["selected_MOS"].append((overall_quality, issues_noticed, pitch_speed_fluency, emotional_expression, voice_pleasantness))
            state["data_store"][state["tester_id"]] = state["selected_MOS"]
            print(f"Tester ID: {state['tester_id']}, Scores: {state['selected_MOS']}")
            with open('res.txt','a') as f:
                text = state['tester_id'] + '\t'
                for s, i, p, e, v in state['selected_MOS']:
                    text += f"{s}({i},{p},{e},{v})\t"
                text += '\n'
                f.write(text)
            state["index"] += 1
            return None, "## Thank you for your feedback! The return code is XXXXX", -1, None, -1, -1, -1, state
        else:
            return None, "## Invalid submission! You can only submitted once per id! The return code is XXXXXX", -1, None, -1, -1, -1, state

    def set_tester_id(self, id, state):
        if id:
            state["tester_id"] = id
            state["selected_MOS"] = []
            state["index"] = 0
            return (
                f"## Your ID: {state['tester_id']}", 
                state, 
                self.current_files[0],  # Reset audio to first file
                f"#### you are rating {state['index']+1} out of {str(len(self.current_files))},after submitting Scroll UP to Step 2 to hear the new audio"  # Reset current file display
            )
        else:
            return "## Please enter a valid ID!", state, None, ""

    def create_interface(self):
        with gr.Blocks() as demo:
            state = gr.State(self.initialize_state())

            gr.Markdown('''
                # Welcome to the Audio Subjective Test
                ## Instructions:
                1. **Before you Start**: Make sure you entered the test id once.
                1. **Listen Carefully**: Play and pay close attention to each audio clip.
                2. **Rate the Audio**: After listening to each audio, assign scores based on the questions provided.
                3. **Submit Your Responses**: Ensure you submit the form before exiting.
            ''')
            
            gr.Markdown("这个部分给众包用的")
            with gr.Row():
                tester_id_input = gr.Textbox(label="Enter Tester ID")
                set_id_button = gr.Button("Set ID")
                id_display = gr.Markdown()
            
            gr.Markdown("------")
            gr.Markdown("## Step 2 Listen Carefully to the following audio: ")
            display_audio = gr.Audio(self.current_files[0], type='filepath')

            gr.Markdown("------")
            gr.Markdown("## Step3 Answer the following questions basing on the audio you hear.")

            gr.Markdown("### I Confirmed that I have read the instructions above and I will take this survey seriously")
            issues_noticed = gr.Radio(
                ["Yes", "No"],
                label="choose Yes/No",
                value=None
            )

            score_description = gr.Markdown("""
                ### 1. On a scale of 1 to 5, How natural (i.e. human-sounding) is this recording？
                | 1 | 2| 3| 4| 5|
                |---|---|---|---|---|
                | Bad|Poor|Fair|Good|Excellent|
                """)

            overall_quality = gr.Slider(minimum=1, maximum=5, step=0.5,
                                value=-1, container=False, interactive=True,
                                label="Overall quality rating")
            
            gr.HTML(self.get_slider_labels_html())

            gr.Markdown("### 2. On a scale of 1 to 5, how would you rate the voice in terms of its speed? Your answer must indicate if you found the speed of delivery of the message appropriate.")
            gr.Markdown('''
                        | 1 | 2| 3| 4| 5|
                        |---|---|---|---|---|
                        | No, too fast|No,too slow|Yes, but faster than preferred|Yes, but slower than preferred|Yes|
                        ''')
            pitch_speed_fluency = gr.Slider(minimum=1, maximum=5, step=1,
                                value=-1, container=False, interactive=True,
                                label="Speaking Rate")
            gr.HTML(self.get_speed_labels_html())
            
            gr.Markdown("### 3. On a scale of 1 to 5, What is the quality of the speech based on the level of distortion of the speech? Your answer must indicate if you noticed any annoying sounds in the speech.")
            gr.Markdown('''
                        | 1 | 2| 3| 4| 5|
                        |---|---|---|---|---|
                        |Bad - Very annoying and objectionable|Poor - Annoying, but not objectionable,|Fair - Perceptible and slightly annoying| Good - Just perceptible, but not annoying|Excellent - Imperceptible|
                        ''')
            emotional_expression = gr.Slider(minimum=1, maximum=5, step=0.5,
                                value=-1, container=False, interactive=True,
                                label="distortion")
            
            gr.HTML(self.get_naturalness_labels_html())

            gr.Markdown("### 4. On a scale of 1 to 5, how would you rate the voice in terms of its voice pleasantness? Your answer must indicate if you found the voice you have heard pleasant.")
            gr.Markdown('''
                        | 1 | 2| 3| 4| 5|
                        |---|---|---|---|---|
                        | Very unpleasant|Unpleasant|Neutral|Pleasant|Very pleasant|
                        ''')
            voice_pleasantness = gr.Slider(minimum=1, maximum=5, step=0.5,
                                value=-1, container=False, interactive=True,
                                label="Voice Pleasantness")
            
            gr.HTML(self.get_pleasantness_labels_html())

            with gr.Row():
                submit = gr.Button("Submit")
            current_file = gr.Markdown("#### Enter your ID before you start or it won't be saved")

            set_id_button.click(
                self.set_tester_id, 
                inputs=[tester_id_input, state], 
                outputs=[id_display, state, display_audio, current_file]
            )
            submit.click(
                self.submit_options, 
                inputs=[overall_quality, issues_noticed, pitch_speed_fluency, emotional_expression, voice_pleasantness, state], 
                outputs=[display_audio, current_file, overall_quality, issues_noticed, pitch_speed_fluency, emotional_expression, voice_pleasantness, state]
            )

        return demo

    @staticmethod
    def get_slider_labels_html():
        return """
        <style>
            .slider-labels {
                display: flex;
                justify-content: space-between;
                margin-top: -10px;
                font-size: 12px;
            }
            .slider-labels div {
                text-align: center;
                width: 5%;
            }
            .slider-labels div:first-child {
                text-align: left;
            }
            .slider-labels div:last-child {
                text-align: right;
            }
        </style>
        <div class="slider-labels">
            <div>1 Bad</div>
            <div>1.5</div>
            <div>2 Poor</div>
            <div>2.5</div>
            <div>3 Fair</div>
            <div>3.5</div>
            <div>4 Good</div>
            <div>4.5</div>
            <div>5 Excellent</div>
        </div>
        """

    @staticmethod
    def get_speed_labels_html():
        return """
        <style>
            .slider-labels {
                display: flex;
                justify-content: space-between;
                margin-top: -10px;
                font-size: 12px;
            }
            .slider-labels div {
                text-align: center;
                width: 10%;
            }
            .slider-labels div:first-child {
                text-align: left;
            }
            .slider-labels div:last-child {
                text-align: right;
            }
        </style>
        <div class="slider-labels">
            <div>1 No, too fast</div>
            <div>2 No,too slow</div>
            <div>3 Yes, but faster than preferred</div>
            <div>4 Yes, but slower than preferred</div>
            <div>5 Yes</div>
        </div>
        """

    @staticmethod
    def get_naturalness_labels_html():
        return """
        <style>
            .slider-labels {
                display: flex;
                justify-content: space-between;
                margin-top: -10px;
                font-size: 12px;
            }
            .slider-labels div {
                text-align: center;
                width: 5%;
            }
            .slider-labels div:first-child {
                text-align: left;
            }
            .slider-labels div:last-child {
                text-align: right;
            }
        </style>
        <div class="slider-labels">
            <div>1 Bad - Very annoying and objectionable</div>
            <div>1.5</div>
            <div>2 Poor - Annoying, but not objectionable</div>
            <div>2.5</div>
            <div>3 Fair - Perceptible and slightly annoying</div>
            <div>3.5</div>
            <div>4 Good - Just perceptible, but not annoying</div>
            <div>4.5</div>
            <div>5 Excellent - Imperceptible</div>
        </div>
        """

    @staticmethod
    def get_pleasantness_labels_html():
        return """
        <style>
            .slider-labels {
                display: flex;
                justify-content: space-between;
                margin-top: -10px;
                font-size: 12px;
            }
            .slider-labels div {
                text-align: center;
                width: 5%;
            }
            .slider-labels div:first-child {
                text-align: left;
            }
            .slider-labels div:last-child {
                text-align: right;
            }
        </style>
        <div class="slider-labels">
            <div>1 Very unpleasant</div>
            <div>1.5</div>
            <div>2 Unpleasant</div>
            <div>2.5</div>
            <div>3 Fair</div>
            <div>3.5</div>
            <div>4 Pleasant</div>
            <div>4.5</div>
            <div>5 Very pleasant</div>
        </div>
        """

if __name__ == "__main__":
    app = MOSApp()
    demo = app.create_interface()
    demo.launch(server_name="0.0.0.0", server_port=25565)
