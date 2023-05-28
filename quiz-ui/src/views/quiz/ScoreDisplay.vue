<template>
    <div class="d-flex flex-column align-content-between" style="width: 60%">
        <div class="form-area shadow-lg center">
            <h1 class ="form-title mb-5"> Scoreboard </h1>
            <h2 class="score-text  mb-5 italic rainbow"> Your score is {{ score }}. </h2>
            <h3 v-for="player in players" :key="player.id" class="sub-title">
                {{ player.name }} : {{ player.score }} points
            </h3>
            <router-link class="button btn-small mt-5" to="/">Return</router-link>
        </div>
    </div>
</template>

<script>
	import participationStorageService from "@/services/ParticipationStorageService.js"
	import quizApiService from "@/services/QuizApiService.js";
	export default {
		name : "ScoreDisplay",
		data() {
			return {
				score: 0,
				players : []
			}
		},
		async created() {
			this.score = participationStorageService.getParticipationScore();
			this.getPlayersData();
		},
		methods: {
			async getPlayersData() {
				const players = await quizApiService.getPlayersData();
				if (players.status !== 200) console.log("ERROR : CAN'T GET PLAYERS DATA");

				this.players = players.data;
			}
		}
	}
</script>

<style>
    .italic {
        font-style: italic;
    }

    .score-text {
        font-family: "Press Start 2p";
        font-size: 12px;
   }

   .rainbow{
		animation: rainbow 2.5s linear;
		animation-iteration-count: infinite;
    }

    @keyframes rainbow{
		100%,0%{
			color: rgb(255,0,0);
		}
		8%{
			color: rgb(255,127,0);
		}
		16%{
			color: rgb(255,255,0);
		}
		25%{
			color: rgb(127,255,0);
		}
		33%{
			color: rgb(0,255,0);
		}
		41%{
			color: rgb(0,255,127);
		}
		50%{
			color: rgb(0,255,255);
		}
		58%{
			color: rgb(0,127,255);
		}
		66%{
			color: rgb(0,0,255);
		}
		75%{
			color: rgb(127,0,255);
		}
		83%{
			color: rgb(255,0,255);
		}
		91%{
			color: rgb(255,0,127);
		}
}
</style>