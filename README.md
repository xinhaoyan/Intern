# Intern
这是本人在2023年12月18日到2024年2月1日 在广州零号科技公司的作为AI算法实习生。 我负责项目是从小说文本中识别出广告的项目 

这个项目主要完成以下的任务：

1. 使用openai.ChatCompletion.create方法对 ``` openai.api_key = "EMPTY" openai.api_base = "http://172.16.16.19X:XXXX/v1" ``` 中的YI大模型进行请求
2. 整个项目中最困难的地方和花费时间最多是 对 Prompt 的调整， 我使用了以下的Prompt Engineering 的技巧：结构化， Few-shot，使用特殊的字符进行分割，以JSON的格式输出等等技巧来提升大模型输出的准确度。
3. 对大文件的处理，原本是仅仅是对抛出异常的文件进行切分，但是经过尝试，最后决定以1000字为上限，按照句子切分，这样既保证了句子语义的完整性以及字数不会超标，取得了非常好的效果。同时对一个chunk中小于500字的进行对上一个chunk的倒数500字抽取补到这个chunk中，对一个chunk中只有一句话的抽取的字数是700字，并且记录原来的chunk的长度（为了输出的时候依然是原文章，不会多）
4. 对一个整的文件夹中的按照数字有序排列的文件进行处理。如果一个整个章节全部只有小于五句话，则把上一个章节的倒数五句话加到这个章节中，之后在章节句数大于5的章节进行记录最后的倒数五句话。之后对大模型输出的JSON的结果进行检测，找到左右大括号，对打括号里面的String 进行``` json.loads ``` 对JSON的格式进行检测，如果报错则对不是JSON中字符串进行修改添加``` 广告内容``` + string 这样就可以转化为JSON正确的形式再输出。最终结果以JSON 文件输出。
5. 将输出的JSON 文件输入，转为DOCX文件，对章节内的广告内容进行标黄。首先手写一个计算两个字符串的最长公共子串长度，并且返回其再str1中的起始位置的函数，用于计算广告在小说中的匹配程度，可以设置不同的阈值来确定什么是完全相同，部分相同，完全不同。这样做的目的是为了防止大模型多输出了一个空格或者句号，换行符让小说文本匹配不到的问题。对于输出为DOCX文件中的部分，要按照之前记录的原本chunk的长度，输出。但是在此之前还需要把广告内容进行过滤，去掉广告部分中不属于原chunk的部分的广告。对于高于阈值的进行标黄。除此之外，本项目还对以下两种特殊情况做出了规避，第一种情况是过滤后广告长度为0了，那么就会输出全篇小说但是没有标黄。第二种情况是大模型输出了一个不在小说中的广告时候。我在输出之前进行预判断，把符合的filename 都保存在一个set集合中，在输出之前进行比对，如果不存在的set集合中filename就不输出。
6. 创建测试集:首先写一个脚本能够从21本小说章节中随机调出400章节，再从这四百章节中随机输出400个chunk，对每一个chunk进行人工找出广告，写到```answer:```之后，以及人工随机找一些具有广告内容的章节。
7. 评估:进行对YI大模型的输出的准确度，精确度，回归率，F1值 进行计算输出，还会统计各种的完全相同章节数，部分相同的章节数以及章节名称，完全不同章节数以及章节名称，方便检查，最后输出为Report.txt。
8. 如果给出一个完整的TXT文件，写把它切割为一个文件夹，里面包含很多txt章节。    

   
