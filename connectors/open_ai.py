import openai

openai.api_key = "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"


class GptAi():
    def __init__(self) -> None:
        pass

    def generate_title(self, prompt: str, tokens=150):

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
text = 'Top cryptos on binance in terms of trading volumes:BTC-TUSD 1.850.534.745$, BTC-USDT  1.129.658.904$, ETH-USDT 449.375.622$'

# text = 'Top gainers Binance:BTC-TUSD volume 1.850.534.745$ '

if __name__ == '__main__':
    fw = GptAi()
    g = f"Comment on this: {text}"
    s = fw.generate_title(g)
    print(s)
