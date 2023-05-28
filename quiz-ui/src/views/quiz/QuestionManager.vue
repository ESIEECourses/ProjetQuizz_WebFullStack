<template>
    <div class="d-flex flex-column align-content-between" style="width: 60%">
        <div class="form-area shadow-lg center">
            <QuestionDisplay :question="currentData" @answer-selected="answerClickedHandler" />
        </div>
    </div>
</template>

<script>
    import quizApiService from "@/services/QuizApiService";
    import participationStorageService from "@/services/ParticipationStorageService";
    import QuestionDisplay from "@/views/quiz/QuestionDisplay.vue";

    export default {
        name: "QuestionManager",
        data() {
            return {
                player: {
                    playerName: "",
                    score: 0
                },
                currentPosition : 1,
                currentData: {
                    title: "",
                    text: "",
                    possibleAnswers: [],
                    image: ""
                }
            }
        },
        components: {
            QuestionDisplay
        },
        // init component
        async created() {
            this.player.playerName = participationStorageService.getPlayerName();
            this.loadQuestionByPos(this.currentPosition);
        },
        methods: {
            async loadQuestionByPos(position) {
                const question = await quizApiService.getQuestion(position);
                if (question.status !== 200) console.log("ERROR : CAN'T LOAD DATA !");
                this.currentData = question.data[0]
            },

            answerClickedHandler(answer) {
                if (this.isCorrect(answer)) this.player.score += 10;

                this.isEnd(this.currentPosition).then((isEnd) =>  {
                    if (isEnd) {
                        this.endQuiz();
                    } else {
                        ++this.currentPosition;
                        this.loadQuestionByPos(this.currentPosition);
                    }
                }) 
            },

            isCorrect(givenAnswer) {
                for (let i = 0; i < this.currentData.possibleAnswers.length; ++i)
                    if (this.currentData.possibleAnswers[i].isCorrect)
                        return i === givenAnswer;  
            },

            async isEnd(position) {
                const info = await quizApiService.getQuizInfo();
                if (info.status !== 200) console.log("ERROR : SERVER NOT AVAILABLE !");

                return info.data.size === position;
            },

            async endQuiz() {
                await quizApiService.setNewPlayer(this.player);
                participationStorageService.saveParticipationScore(this.player.score);
                this.$router.push('/scoreboard');
            }
        }

    };

</script>

<style>
    .hidden {
       visibility: hidden; 
    }
</style>