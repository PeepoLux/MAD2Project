Vue.component('list_venues', {
    template: `
            <div>
            
            <div v-for="(item, index) in value">

            <div v-if="city_chosen == item[2] || city_chosen == "None"">
            
            <div class="container">

            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">{{ item[0] }}</h5>
                    <b>Place: </b>
                    <h7 class="card-title ">{{ item[1] }}</h7>
                    <br>
                    <b>City: </b>
                    <h7 class="card-title ">{{ item[2] }}</h7>
                    <br>
                    <b>Capacity: </b>
                    <h7 class="card-title ">{{ item[3] }}</h7>
                    <br>

                </div>

                <div  v-if="item[5] > 0">

                <p>
                    <button id="mycheat1" class="btn btn-primary" type="button" data-bs-toggle="collapse"
                        data-bs-target="#collapse{{item[4]}}WidthExample" aria-expanded="false"
                        aria-controls="collapse{{item[4]}}WidthExample">
                        View Shows
                    </button>
                </p>

                <div class="collapse collapse-horizontal" id="collapse{{item[4]}}WidthExample">
                    <div class="container text-center">
                        <div class="row">
                            <div v-for="(show, index) in item[6]">
                            <div v-if="show[1].includes(tags_chosen) || tags_chosen == "None"">
                            <div v-if"show[3] >= rating_chosen">
                            <div class="col">
                                <div class="card card-body" style="width: 300px;">
                                    <h5 class="card-title">{{ show[0] }}</h5>
                                    <b>Tags: </b>
                                    <h7 class="card-title ">{{ show[1] }}</h7>

                                    <b>Price(in INR): </b>
                                    <h7 class="card-title ">{{ show[2] }}</h7>

                                    <b>Rating(on 5): </b>
                                    <h7 class="card-title ">{{ show[3] }}</h7>
                                    <b>Time: </b>
                                    <h7 class="card-title ">{{ show[4] }} - {{ show[5] }}</h7>


                                    <div class="center">
                                        <div v-if="show[7] != 0">
                                        <button type="button" class="btn btn-success" data-bs-toggle="modal"
                                            data-bs-target="#exampleshow{{show[6]}}Modal3" :value="show[6]"
                                            id="time_button" onclick="setTimer(this)">
                                            Book
                                        </button>
                                        </div>
                                        <div v-else>
                                        <button type="button" class="btn btn-danger" data-bs-toggle="modal"
                                            data-bs-target="#exampleshow{{show[6]}}Modal3" :value="show[6]"
                                            id="time_button" onclick="setTimer(this)" disabled>
                                            Full House
                                        </button>
                                        </div>
                                        <!-- Modal -->
                                        <div class="modal fade" data-bs-backdrop="static" id="exampleshow{{show[6]}}Modal3"
                                            tabindex="-1" aria-labelledby="exampleModalLabel3" aria-hidden="true">
                                            <div class="modal-dialog">
                                                <div class="modal-content">
                                                    <div class="modal-header">
                                                        <h1 class="modal-title fs-5" id="exampleModalLabel3">Booking
                                                        </h1>


                                                        <button onclick="window.location.reload();" type="button"
                                                            class="btn-close" data-bs-dismiss="modal" aria-label="Close">
                                                        </button>
                                                    </div>
                                                    <!-- Add the timer here -->

                                                    <p class="alert alert-danger" role="alert" id="{{show[6]}}demo"></p>

                                                    <form method="POST" action="/booking">

                                                        <div class="form-outline mb-3">
                                                            Show:
                                                            <input type="hidden" v-model="venue_id" name="venue_id"> {{item[4]}} </input>
                                                            <input type="hidden" :value="show[6]" v-model="show_id" name="show_id" />

                                                            <input type="text" name="show_name" :value="show[0]"
                                                                id="form3example4" class="form-control form-control-lg"
                                                                disabled />
                                                        </div>
                                                        <div class="form-outline mb-3">
                                                            Venue: <input type="text" name="venue_name"
                                                                :value="item[0]" id="form3example4"
                                                                class="form-control form-control-lg" disabled />
                                                        </div>

                                                        <div class="form-outline mb-3">
                                                            Price: <input type="text" id="{{show[6]}}price"
                                                                name="show_price" :value="show[2]"
                                                                class="form-control form-control-lg" disabled />
                                                        </div>

                                                        <div class="form-outline mb-3">
                                                            Available Seats: <input type="text" v-model="available_seats" name="available_seats"
                                                                :value="show[7]" id="form3example4"
                                                                class="form-control form-control-lg" disabled />
                                                        </div>
                                                        <input type="hidden" id="{{show[6]}}available_seats"
                                                            name="available_seatss" :value="show[7]" />
                                                        Number of Seats:
                                                        <div class="btn-toolbar" role="toolbar"
                                                            aria-label="Toolbar with button groups">
                                                            <div class="btn-group me-2" role="group"
                                                                aria-label="First group">
                                                                <button onclick="setAmount(this)" :value="show[6]"
                                                                    type="button" class="btn btn-primary">1</button>
                                                                <button onclick="setAmount(this)" type="button"
                                                                    :value="show[6]" class="btn btn-primary">2</button>
                                                                <button onclick="setAmount(this)" type="button"
                                                                    :value="show[6]" class="btn btn-primary">3</button>
                                                                <button onclick="setAmount(this)" type="button"
                                                                    :value="show[6]" class="btn btn-primary">4</button>
                                                                <button onclick="setAmount(this)" type="button"
                                                                    :value="show[6]" class="btn btn-info">5</button>
                                                                <button onclick="setAmount(this)" type="button"
                                                                    :value="show[6]" class="btn btn-info">6</button>
                                                                <button onclick="setAmount(this)" type="button"
                                                                    :value="show[6]" class="btn btn-info">7</button>
                                                                <button onclick="setAmount(this)" type="button"
                                                                    :value="show[6]" class="btn btn-info">8</button>
                                                                <button onclick="setAmount(this)" type="button"
                                                                    :value="show[6]" class="btn btn-info">9</button>
                                                            </div>
                                                        </div>

                                                        <div class="form-outline mb-3">
                                                            Total Amount: <input type="text" name="total_amount" value=""
                                                                id="{{show[6]}}total_amount"
                                                                class="form-control form-control-lg" disabled />
                                                        </div>
                                                        <input type="hidden" id="{{show[6]}}seats" v-model="seats" name="seats" value="" />


                                                        <div class="modal-footer">
                                                            <button type="button" onclick="window.location.reload()"
                                                                class="btn btn-danger" data-bs-dismiss="modal">No</button>
                                                            <button v-on:click="make_booking" name="Go" class="btn btn-success">Yes</button>

                                                        </div>
                                                    </form>
                                                </div>
                                            </div>
                                        </div>

                                    </div>

                                </div>
                            </div>   
                            </div>
                            </div>
                            </div>
                        </div>
                    </div>
                </div>
                </div>
                <div v-else>
                <h5>No Shows Exist</h5>
                </div>


            </div>
        </div>
        </div>
        </div>

        </div>
      `,
    data: function () {
        return {
            message: "Hello World",
            venue_id: null,
            show_id: null,
            seats: null,
            available_seats: null
        }
    },
    methods: {
        make_booking: function () {

            const res = fetch("http://localhost:5000/api/makebooking", {
                method: "POST",
                headers: {
                    'show_id': this.show_id,
                    'venue_id': this.venue_id,
                    'seats': this.seats,
                    'available_seats': this.available_seats
                }
            })
            .then(response => response.json())
            .then(function (data) {
                if (data["status"] == 1) {
                    window.location.href = 'http://localhost:5000/home'
                }
            })


            // const data = res.json()
            // this.output = data['status']
            // window.location.href = 'http://localhost:5000/home'
        }
    }
})

var app = new Vue({
    el: "#app",
  })