from django.shortcuts import render


from .source.sentiment import Sentiment
import time
t = time.time()

# print(Sentiment('The best love is the kind that awakens the soul; that makes us reach for more, that plants the fire in our hearts and brings peace to our minds. That’s what I hope to give you forever').get_mood())
# print('---', time.time() - t)


def textplay(request):
    sentence = request.GET.get('sentence', None)
    print(sentence)
    # sentence = 'akash jain'
    if sentence is not None:
        sent_ins = Sentiment(sentence)
        print(sentence)
        polarity = sent_ins.get_polarity()
        # mood = sent_ins.get_mood()
        mood = ''
        return render(request, 'index.html', {'polarity': polarity, 'mood': mood})
    else:
        return render(request, 'index.html')
