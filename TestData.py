import json
import openai

## TestData 函数
def longest_common_substring(str1, str2):
    # 构建一个二维数组来保存两个字符串的字符匹配情况
    dp = [[0] * (len(str2) + 1) for _ in range(len(str1) + 1)]
    max_length, end_index = 0, 0

    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_length:
                    max_length = dp[i][j]
                    end_index = i
            else:
                dp[i][j] = 0

    # 返回最长公共子串
    return str1[end_index - max_length: end_index]

def calculate_similarity(str1, str2, lcs):
    average_length = (len(str1) + len(str2)) / 2
    return len(lcs) / average_length if average_length > 0 else 0

openai.api_key = "EMPTY"
openai.api_base = "http://172.16.16.195:8001/v1"

def get_completion(message, model="/data/models/01-Yi/Yi-34B-Chat"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=message,
        max_tokens=1000,
        top_p=0.8,
        temperature=0.1,
        stop_token_ids=[7],
        stream=True,
    )
    full_message = ""
    for chunk in response:
        if "content" in chunk.choices[0].delta.keys() and chunk.choices[0].delta.content is not None:
            full_message += chunk.choices[0].delta.content
            
    
    return full_message


def process_chunk(chunk):
    #创建包含系统和用户信息的message列表
    message = [
    {
      "role": "system",
      "content": "任务说明：\n作为小说网站的管理员，你的任务是识别并提取网络流行小说中的广告内容。请根据以下步骤和标准来分析文本，并确定是否存在广告：\n\n- 广告只会位于小说的开头或结尾，并可能以特定标志如'PS:'，'【'，'（'，'——'等开头。\n\n- 广告内容主要是小说作者为了推广而与读者互动的部分，与小说情节发展无关。互动语气包括但不限于“祈求”，“评论”，“批评”，“祝福”。“问候”。\n\n- 广告一般只有一句话，简洁明了。但是偶尔小说中广告会出现多句话，如果你判断小说中的广告为多句话为广告，请你谨慎判断，确保不会把小说内容识别为广告词。\n\n- 广告可能包括作者推荐小说的句子、打赏要求，或对小说内容的说明、解释和评价。\n\n- 注意，大部分小说内是没有广告的，请不要过度解读，从而把小说内容误解成广告。\n\n请在分析小说内容时，特别注意区分广告内容和正文，重点关注以特定标志开始的段落和与小说情节无关的简短互动性语句。\n\n---\n\n请你按照以下的步骤来找出广告：\n\n1.阅读一段连载小说的文本，注意其叙述风格和结构。\n\n2.识别文本中可能的风格变化和与主故事线不一致的元素。\n\n3.特别关注文末内容，判断是否有作者直接与读者互动的部分，或者是否包含广告语言和非故事元素。\n\n4. 分析这些元素是否构成广告或仅仅是作者试图增加读者互动的方式。\n\n【以下为小说内容：】\n### 您的小说文本 ###\n---\n在分析后，模型应按照JSON的格式输出：\nKey  为\\\\\\\"广告内容\\\\\\\"， Value 为识别到的广告内容或者\\\\\\\"无广告\\\""
    },
    {
      "role": "user",
      "content": """ <小说文本示例1>:'''过了一会男人又发了信息过来，问顾念下榻的酒店叫什么。\n    顾念还真的没注意这个，她翻了翻子豪发给她的信息。\n    子豪给她订的酒店，据说正好沿海，开窗就能看见不远处的海边。\n    关于下榻酒店的事情，她就不太想和这男人说了。\n    为了防止男人再纠缠，她说自己有朋友在三亚，说朋友会过来接她。\n    回了信息之后，顾念就把手机放下了。\n    眼角有些不自觉的又瞄了一下池遇。\n    池遇一直没反应，好像是对她这边的动静一点也不关心。\n    顾念突然就觉得有些无趣。\n    想起之前两个人在婚姻存续期间内，自己出门被人搭讪，池遇知道后都没什么反应。\n    如今这样，也算是正常了。\n    因为不爱，所以能不被影响。\n    这个认知，真的是让顾念心里不舒服的很。\n    在之前将近一年的时间内，她不是没努力过。\n    只是池遇真的是一块难啃的骨头。\n PS：请大家看清楚了，顾念可不是好人啊'''"""
    },
    {
      "role": "assistant",
      "content":  """{"广告内容":"PS：请大家看清楚了，顾念可不是好人啊"}"""
    }, 
    {
      "role": "user",
      "content": """<小说文本示例2>:'''PS: 最近太累啦，随便写写\n————\n先行是近几年在超一线城市迅速崛起并被富人极力追捧的教育机构，业内称其为天才集中营，外界则戏称烧钱大本营，诉其集嫌贫爱富和攀高结贵于一体。\n    虽风评天差地别，但没人可以否认先行在教育行业的突出表现。先行主要服务面临中高考的学生，承诺无论基础如何，保证最迟一年时间考上满意院校。\n    创办整三年，承诺百分百兑现，引来大批望子成龙的富人拿着钱排队预约，当普通人还在花着大把时间拼着不确定的未来时，有些人早已拿钱买注定灿烂的未来了。\n    早上八点多，闵姜西出现在cbd最豪华地段，买了早餐和牛奶，预留出跟几十上百号人争抢电梯的时间，来到公司的时候，距离正式上班还有十几分钟。\n    往常的清晨总是最百无聊赖的时刻，即便早到的人也都坐在各自的座位上，或对着镜子补妆，或对着电脑补课，静得像是临近高考的实验班，然而今天情况很是特殊，闵姜西一推门便看到一帮人聚在一起，似乎发生了什么大事儿。'''"""
    },
    {
      "role": "assistant",
      "content": """{"广告内容":"PS: 最近太累啦，随便写写"}"""
    },
    {
        "role": "user",
        "content": """ <小说文本示例3>:'''闵姜西看着不动声色，实则心底警铃大作，她突然想到昨晚她在车上，秦佔发给她的那条短信，陆遇迟装警察的事情，原本只有他们两个知道，可秦佔却神不知鬼不觉的发现了。\n    她不确定秦佔是什么时候知晓的，是只查了陆遇迟一个人，还是像外界传言的那般，秦佔所在的方圆千米内，不可能有身份可疑的人，就怕对他图谋不轨。\n    不管是碰巧还是意料之中，越是跟秦佔接触，闵姜西就越觉着传言非虚，怪不得程双光是听到他的名字就如临大敌。\n    短暂的如鲠在喉，闵姜西很快便强迫自己镇定对应:“谢谢秦先生给我机会，我会努力成为自己人。”\n    秦佔抽了最后一口烟，将烟头按灭在一旁的灭烟器中，淡淡道:“明天上午十点。”\n    闵姜西点头应声，“好。”'''"""
    },
    {
        "role": "assistant",
        "content": """{"广告内容":"无广告"}"""
    },
    {
        "role": "user",
        "content": f"""<小说文本示例4>: '''{chunk}'''"""
    }
        ]
    return {"result": get_completion(message, model="/data/models/01-Yi/Yi-34B-Chat"), "chunk": chunk}

def Test_Process(json_file_path, output_file, report_file):
    # 读取 JSON 文件
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    results = []
    FN = 0
    FP = 0
    exact_match = 0
    partial_match = 0
    no_match = 0
    partial_match_files = []
    no_match_files = []

    for item in data:
        filename = item["chunkname"]
        chunk = item["chunk"]
        answer = item["answer"].replace('\n', '')  # 移除换行符
        try:
            # 处理每个 chunk
            chunk_data = process_chunk(chunk)
            result = chunk_data["result"].replace('\n', '')  # 移除换行符
            item["result"] = result
            results.append(item)

            # 使用 SequenceMatcher 比较 answer 和 result
            lcs = longest_common_substring(answer, result)
            similarity = calculate_similarity(answer, result, lcs)
            if similarity >=0.8:
                exact_match += 1
            elif similarity > 0.3 and answer != result and len(answer)>3 and len(result)>3:  # 设置一个阈值
                partial_match += 1
                partial_match_files.append(filename)
            elif similarity > 0.5 and answer != result and (len(answer) < 3 or len(result) < 3):
                partial_match += 1
                partial_match_files.append(filename)
            else:
                no_match += 1
                no_match_files.append(filename)
            if answer !="{\"广告内容\":\"无广告\"}" and result =="{\"广告内容\":\"无广告\"}":
                FN +=1
            if answer =="{\"广告内容\":\"无广告\"}" and result !="{\"广告内容\":\"无广告\"}":
                FP +=1
            # 打印每次处理后的结果
            print(f"Processed {filename}: {result}")
        except Exception as e:
            print(f"处理 {filename} 时发生错误: {e}")
            continue

    total_processed = len(data)
    accuracy = exact_match / total_processed if total_processed > 0 else 0
    #寻找FN,计算recall
    recall = exact_match / (exact_match + FN) if (exact_match + FN) > 0 else 0
    
    precision = exact_match / (exact_match + FP) if (exact_match + FP) > 0 else 0

    F1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    # 保存结果
    if results:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        print(f"Results saved to {output_file}")

        # 写入报告
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"Total Processed: {total_processed}\n")
            f.write(f"Exact Match: {exact_match}\n")
            f.write(f"Partial Match: {partial_match}\n")
            f.write(f"No Match: {no_match}\n")
            f.write(f"Accuracy: {accuracy:.2f}\n")  # 保留两位小数
            f.write(f"Recall: {recall:.2f}\n")  # 保留两位小数
            f.write(f"Precision: {precision:.2f}\n")  # 保留两位小数
            f.write(f"F1_score: {F1_score:.2f}\n")  # 保留两位小数
            f.write(f"Partial Match Files: {', '.join(partial_match_files)}\n")
            f.write(f"No Match Files: {', '.join(no_match_files)}\n")
        print(f"Report saved to {report_file}")
    else:
        print("No valid chunks to process.")

# 示例用法
json_file_path = "TestChunk.json"
output_file = "ProcessedResults.json"
report_file = "report.txt"
Test_Process(json_file_path, output_file, report_file)
