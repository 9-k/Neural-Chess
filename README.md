# Neural-Chess
Keras based neural chess evaluator. Highly based on Erik Bernhardsson's Deep Pink, see [here](https://erikbern.com/2014/11/29/deep-learning-for-chess). If anyone is ever looking at this, please don't just copy and paste it into your computer and expect it to work. Lots of this is hacky and hardcoded, so it really will be a struggle to get it to work on your machine. Also, the parse_game script will take like 6 hours to generate your training data. I tried to optimize it but I'm a physics major for goodness' sake, so don't expect too much! Oh! Additionally, this model is a binary classifier - it should output 1 if it thinks White wins and 0 if Black wins. The training data includes the early game, where it is VERY unclear, so the binary accuracy really won't get too good. If I were to redo this, I would definitely cut out the early game from the training data. Good luck!
