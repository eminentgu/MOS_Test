import gradio as gr

class MOSApp:
    # ... (保持其他方法不变)

    def submit_options(self, option, issues_noticed, state):
        if not state["tester_id"]:
            return None, "Please enter your tester ID first.", -1, False, state

        if state["index"] < len(self.current_files) - 1:
            state["selected_MOS"].append((option, issues_noticed))
            state["index"] += 1
            current_audio = self.current_files[state["index"]]
            return current_audio, f"#### you are rating {state['index']+1} out of {str(len(self.current_files))},after submitting Scroll UP to Step 2 to hear the new audio", -1, False, state
        elif state["index"] == len(self.current_files) - 1:
            state["selected_MOS"].append((option, issues_noticed))
            state["data_store"][state["tester_id"]] = state["selected_MOS"]
            print(f"Tester ID: {state['tester_id']}, Scores: {state['selected_MOS']}")
            with open('res.txt','a') as f:
                text = state['tester_id'] + '\t'
                for s, i in state['selected_MOS']:
                    text += f"{s}({'Yes' if i else 'No'})\t"
                text += '\n'
                f.write(text)
            state["index"] += 1
            return None, "## Thank you for your feedback! The return code is XXXXX", -1, False, state
        else:
            return None, "## Invalid submission! You can only submitted once per id! The return code is XXXXXX", -1, False, state

    def create_interface(self):
        with gr.Blocks() as demo:
            state = gr.State(self.initialize_state())

            # ... (保持前面的代码不变)

            gr.Markdown("## Step3 Answer the following questions based on the audio you hear.")
            score_description = gr.Markdown("""
                ### 1.  How would you rate the overall quality of the voice, in terms of its naturalness, intelligibility, and pronunciation?
                | Score | How natural / human | How Robotic |
                |-------|---------------------|-------------|
                | 5 Excellent | Completely natural speech | Imperceptible |
                | 4 Good | Mostly natural speech | Just perceptible but not annoying |
                | 3 Fair | Equally natural and unnatural | Perceptible and slightly annoying |
                | 2 Poor | Mostly unnatural speech | Annoying, but not objectionable |
                | 1 Bad | Completely unnatural speech | Very annoying and objectionable |

                ### Rating the Confidence Level of Each Recording
                """)
            options = gr.Slider(minimum=1, maximum=5, step=0.5,
                                value=-1, container=False, interactive=True)
            
            gr.HTML(self.get_slider_labels_html())

            issues_noticed = gr.Checkbox(label="Were there any specific issues you noticed in the voice, such as unnatural intonation, pauses, or robotic-sounding speech?")
            
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
                inputs=[options, issues_noticed, state], 
                outputs=[display_audio, current_file, options, issues_noticed, state]
            )

        return demo

# ... (保持其他代码不变)


score_description = gr.Markdown("""
                ### 1.  How would you rate the overall quality of the voice, in terms of its naturalness, intelligibility, and pronunciation?
                | Score | How natural / human | How Robotic |
                |-------|---------------------|-------------|
                | 5 Excellent | Completely natural speech | Imperceptible |
                | 4 Good | Mostly natural speech | Just perceptible but not annoying |
                | 3 Fair | Equally natural and unnatural | Perceptible and slightly annoying |
                | 2 Poor | Mostly unnatural speech | Annoying, but not objectionable |
                | 1 Bad | Completely unnatural speech | Very annoying and objectionable |

                ### Rating the overall quality of the voice, in terms of its naturalness, intelligibility, and pronunciation
                """)
