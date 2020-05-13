# Pseudo-Grammarly-for-Transcriptions
This is a rule based grammar corrector for speech-transcriptions, written-transcriptions, (.wav) file's transcriptions.
This architecture was constructed with combinations of some traditional Information Retrieval approaches like Soundex with some enhancements that were not there in the actual algorithm, Levenshtein's distance and Google's Speech API was imported for performing ASR. If there is a mistake/error in the transcription (like the word in transcription is absent in the English Dictionary), then it will give the most possible solutions by suggesting the best choices of words that can replace the wrong word. I have not created an UI, so every action is console-based. In this application, you see three advantages:
                  1. To correct the speech based transcriptions
                  2. To correct the (.wav) file transcriptions
                  3. To correct the written transcriptions (i.e. again speech transcriptions but already available in written form)
