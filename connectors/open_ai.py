import openai

openai.api_key = "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"


class GptAi():
    def __init__(self) -> None:
        pass

    def generate_title(self, prompt: str, tokens=250):

        prev_headings = []
        final_heading = ''
        for headings in range(10):
            temp_text = prompt
            temp_text = temp_text + f'[{", ".join(prev_headings)}]'
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=temp_text,
                max_tokens=tokens,
                n=5,
                temperature=1,
                )

            headings2 = [lst.text.replace("\n\n", '') for lst in response.choices]
            best_heading = max(headings2, key=len)
            prev_headings.append(best_heading)

        for find_best_heading in prev_headings:
            if len(find_best_heading) > len(final_heading):
                final_heading = find_best_heading
        
        return final_heading
        


if __name__ == '__main__':
    fw = GptAi()
    g = f"Write the headline that stock exchange NYSE closed with a quote reading of 2.75%."\
                    f"And add a closed lock emoji to the beginning of the header in this format '&#x1F512; ' The headline should be short, catchy and unique, unlike any of the previous ones: "

    s = fw.generate_title(
        g
    )
    print(s)