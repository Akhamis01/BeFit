// This JS file is used for the 'recipe.html' file, to create the PieChart function, and Carousel, and for fetching the Edamam API
// The Edamam API is used to create the recipe cards at the bottom of the page, and is used to generate a 'Meal of the day' when going to next slide in the carousel
// Also implements dynamic reloading functionality, and adds some loading sequences to a few functions

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#weight-btn').addEventListener('click', () => Piechart());
    document.querySelector('#next-caro').addEventListener('click', () => {
        document.querySelector('#carousel-innerid').classList.add('show');
        setTimeout(function() {
            APICarousel();
        }, 2000);
    })

    let search = document.querySelector('#search')
    search.addEventListener('click', () => {
        card_num = 0
        $("html, body").animate({ scrollTop: '+=100' }, 1000);
        sendAPIrequest(card_num)
    })

    let apply_filter = document.querySelector('#apply-filter')
    apply_filter.addEventListener('click', () => {
        card_num = 0
        $("html, body").animate({ scrollTop: '+=100' }, 1000);
        SendAPIFilter(card_num)
    })


    nav_disable = document.querySelector('#nav-disabled')
    nav_disable.addEventListener('click', () => {
        console.log('lol')
        document.querySelector('#alert').style.display = 'block';

        setTimeout(function() {
            $('#alert').fadeOut('slow');
        }, 1500);
    })
    
});





async function APICarousel(){
    let APP_ID = '' // Input here your API ID
    let API_KEY = '' // Input here your API KEY
    const list_of_foods = ['egg', 'meat', 'pizza', 'fish']
    const random_food = Math.floor(Math.random() * list_of_foods.length);
    const count = 12
    num = Math.floor(Math.random() * count);
    document.querySelector('#carousel-innerid').classList.add('show');

    let response = await fetch(`https://api.edamam.com/search?app_id=${APP_ID}&app_key=${API_KEY}&q=${list_of_foods[random_food]}&from=${num}`)
    let data = await response.json()
    console.log(data)

    diet_label = 'None'
    if(data.hits[0].recipe.dietLabels.length != 0){
        diet_label = data.hits[0].recipe.dietLabels[0]
    }
    
    document.querySelector('#carousel-innerid').innerHTML = `
        <div class="carousel-item active">
            <img id="food-img" src="${data.hits[0].recipe.image}" class="d-block w-100">
            <div id="caption" class="carousel-caption" style="background: rgba(0,0,0,.5);">
                <h5>${data.hits[0].recipe.label}</h5>
                <p class="parg">Calories: ${parseFloat(data.hits[0].recipe.calories).toFixed(2)}</p>
                <p>Diet Label: ${diet_label}</p>
            </div>
        </div>
    </div>`

    setTimeout(function() {
        document.querySelector('#carousel-innerid').classList.remove('show');
    }, 500);
}






function Piechart(){
    document.getElementById("piechart").innerHTML = ''
    document.querySelector('#tips').innerHTML = ''
    console.log(document.querySelector('#logged_in').innerHTML)
    $('.load-wrapper1').fadeIn('slow', function(){
        $('.load-wrapper1');
    });
    setTimeout(function() {
        if(document.querySelector('#logged_in').innerHTML == 'true'){
            let weight = document.querySelector('#weight-input').value;
            const current_weight = document.querySelector('#current-weight').innerHTML;
            const recom_calories = document.querySelector('#recom-calories').innerHTML;
            if(weight > 130 || weight < 30){
                document.getElementById("piechart").innerHTML = '<h5 class="alert alert-warning" style="text-align: center; margin-right: 20%;">Chart unavailable for inputted value, please select a weight between 30-130 kg</h5>'
            } else{
                document.getElementById("piechart").innerHTML = '<canvas id="pieChart"></canvas>';
                var ctxP = document.getElementById("pieChart").getContext('2d');
                protein = 0.71 * weight;
                fat = 78 - (weight * 0.45);
                sugar = 60 - (weight * 0.3);
                carbs = 170 - (weight * 1.2);
                fiber = 32 + (weight * 0.07)
                    var myPieChart = new Chart(ctxP, {
                        type: 'pie',
                        data: {
                                labels: ["Protein", "Fats", "Carbs", "Fiber", 'Sugars'],
                                datasets: [{
                                        data: [protein.toFixed(2), fat.toFixed(2), carbs.toFixed(2), fiber.toFixed(2), sugar.toFixed(2)],
                                        backgroundColor: ["#F7464A", "#46BFBD", "#FDB45C", "#949FB1", "#4D5360"],
                                        hoverBackgroundColor: ["#FF5A5E", "#5AD3D1", "#FFC870", "#A8B3C5", "#616774"]
                                    }]
                            },
                        options: {
                            responsive: true
                        }
                    });

                    if(weight > parseInt(current_weight)){
                        document.querySelector('#tips').innerHTML = `
                        <div style="background-color: rgb(232, 248, 253); padding: 1rem;">
                            <h3 style="margin-bottom: 0;">Tips to gain weight:</h3>
                            <hr>
                            <h5 class="small" style="color: grey;">To maintain your weight, you must ingest ${recom_calories} Calories per day.</h5>
                            <ul>
                                <li>Must keep a caloric surplus</li>
                                <li>Do cardio once a week to stay healthy</li>
                                <li>Eat clean and healthy, avoid the junk food!</li>
                                <li>Drink 2 litres of water a day</li>
                                <li>Excercise 2-3 times a week</li>
                                <li>Set daily goals and reminders!</li>
                            </ul>
                        </div>`
                    } else if(weight < parseInt(current_weight)){
                        document.querySelector('#tips').innerHTML = `
                        <div style="background-color: rgb(232, 248, 253); padding: 1rem;">
                            <h3 style="margin-bottom: 0;">Tips to lose weight:</h3>
                            <hr>
                            <h5 class="small" style="color: grey;">To maintain your weight, you must ingest ${recom_calories} Calories per day.</h5>
                            <ul>
                                <li>Must staying under your maintainance amount of calories</li>
                                <li>Do cardio 4-5 times week to stay healthy</li>
                                <li>Eat clean and healthy, avoid the junk food!</li>
                                <li>Have salads daily!</li>
                                <li>Drink 3 litres of water a day</li>
                                <li>Excercise 4-5 times a week</li>
                                <li>Set daily goals and reminders!</li>
                            </ul>
                        </div>`
                    }
            }
        } else if(document.querySelector('#logged_in').innerHTML == 'false'){
            document.getElementById("piechart").innerHTML = '<h5 class="alert alert-warning" style="text-align: center; margin-right: 20%;">Must be logged in to use this feature.</h5>'
        }
    }, 1500);
    $('.load-wrapper1').fadeIn('slow', function(){
        $('.load-wrapper1').delay(500).fadeOut();
    });
}




async function sendAPIrequest(card_num){
    card_num += 12;
    //Edamam API Details are stored in the next 2 variables.
    let APP_ID = '' // Input here your API ID
    let API_KEY = '' // Input here your API KEY
    const query = document.querySelector('#recipe_query').value;
    if(card_num == 12){
        $('.load-wrapper').fadeIn('slow', function(){
            $('.load-wrapper').delay(1000);
        });
    } else{
        $("html, body").animate({ scrollTop: '+=50' }, 1000);
        $('.load-wrapper2').fadeIn('slow', function(){
            $('.load-wrapper2').delay(1000);
        });
    }
    // recipe_id = '2f39aece175792d4909f91b0073979c7'
    // let response = await fetch(`https://api.edamam.com/search?app_id=${APP_ID}&app_key=${API_KEY}&r=http%3A%2F%2Fwww.edamam.com%2Fontologies%2Fedamam.owl%23recipe_${recipe_id}`)
    let response = await fetch(`https://api.edamam.com/search?app_id=${APP_ID}&app_key=${API_KEY}&q=${query}&from=0&to=${card_num}`)
    let data = await response.json()
    console.log(data)
    useAPIdata(data, card_num, 'without-filter')
}




async function SendAPIFilter(card_num){
    card_num += 12;
    let APP_ID = '' // Input here your API ID
    let API_KEY = '' // Input here your API KEY
    const query = document.querySelector('#recipe_query').value;
    temp_ingr_num = document.querySelector('#ingr-filter').value;
    temp_cook_num = document.querySelector('#time-filter').value;
    temp_diet_val = document.querySelector('#diet-filter').value;
    temp_health_val = document.querySelector('#health-filter').value;
    let final_filter = ''

    if(temp_ingr_num != ''){
        final_filter += `&ingr=${temp_ingr_num}`
    }
    if(temp_cook_num != ''){
        final_filter += `&time=${temp_cook_num}%2B`
    }
    if(temp_diet_val != 'Any'){
        final_filter += `&diet=${temp_diet_val}`
    }
    if(temp_health_val != 'Any'){
        final_filter += `&health=${temp_health_val}`
    }

    if(card_num == 12){
        $('.load-wrapper').fadeIn('slow', function(){
            $('.load-wrapper').delay(1000);
        });
    } else{
        // $("html, body").animate({ scrollTop: '+=50' }, 1000);
        $('.load-wrapper2').fadeIn('slow', function(){
            $('.load-wrapper2').delay(1000);
        });
    }

    let response = await fetch(`https://api.edamam.com/search?app_id=${APP_ID}&app_key=${API_KEY}&q=${query}&from=0&to=${card_num}` + final_filter)
    let data = await response.json()
    console.log(final_filter)
    console.log(data)
    useAPIdata(data, card_num, 'with-filter')
}







function useAPIdata(data, card_num, filter){
    if(data.count >=12){
        _scroll = true;
        var search = '<div class="row">';
        for(i=0; i<card_num; i++){
            
            health_label = ''
            for(j=0; j<data.hits[i].recipe.healthLabels.length; j++){
                health_label += (data.hits[i].recipe.healthLabels[j] + ', ')
            }
            health_label = health_label.slice(0,-2)

            diet_label = 'None'
            if(data.hits[i].recipe.dietLabels.length != 0){
                diet_label = data.hits[i].recipe.dietLabels[0]
            }

            if(i%4 == 0 && i!=0){
                search += `</div><div class="row">` + `<div class="col-lg-3 col-md-6 col-sm-6 col-12">
                    <div id="card-recipe" class="card shadow p-3 mb-5 bg-white rounded cards" style="width: 20rem;">
                        <img class="card-img-top" src="${data.hits[i].recipe.image}" style="height: 10rem;">
                        <div class="card-body">
                            <hr>
                            <h5 class="card-title">${data.hits[i].recipe.label}</h5>
                            <button type="button" id="card-food" data-id="${i}" class="btn btn-outline-info btn-recipe inner-button" data-toggle="modal" data-target="#exampleModal-${i}">More Info!</button>
                
                            <div class="modal fade" id="exampleModal-${i}" data-backdrop="static" data-keyboard="false" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title" id="exampleModalLabel">${data.hits[i].recipe.label}</h5>
                                            <button id="btn-close-${i}" type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                                        </div>
                                        <div class="modal-body">
                                            <p><span style="color: red;">* Calories:</span> ${parseFloat(data.hits[i].recipe.calories).toFixed(2)} Kcal</p>
                                            <hr>
                                            <p class="parg fontt"><span style="color: red;">- Protein:</span> ${parseFloat(data.hits[i].recipe.digest[2].total).toFixed(2)} g</p>
                                            <p class="parg fontt"><span style="color: red;">- Fats:</span> ${parseFloat(data.hits[i].recipe.digest[0].total).toFixed(2)} g</p>
                                            <p class="fontt"><span style="color: red;">- Carbs:</span> ${parseFloat(data.hits[i].recipe.digest[1].total).toFixed(2)} g</p>
                                            <hr>
                                            <p class="parg fontt"><span style="color: red;">- Health Label(s):</span> ${health_label}</p>
                                            <p class="fontt"><span style="color: red;">- Diet Label:</span> ${diet_label}</p>
                                            <p class="fontt"><span style="color: red;">- Number of ingredients used:</span> ${data.hits[i].recipe.ingredients.length} Ingredients</p>
                                        </div>
                                        <div class="modal-footer">
                                            <a href="${data.hits[i].recipe.url}" class="btn btn-outline-info">Check Recipe!</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>`
            } else{
                search += `<div class="col-lg-3 col-md-6 col-sm-6 col-12">
                    <div id="card-recipe" class="card shadow p-3 mb-5 bg-white rounded cards" style="width: 20rem;">
                        <img class="card-img-top" src="${data.hits[i].recipe.image}" style="height: 10rem;">
                        <div class="card-body">
                            <hr>
                            <h5 class="card-title">${data.hits[i].recipe.label}</h5>
                            <button type="button" id="card-food" data-id="${i}" class="btn btn-outline-info btn-recipe inner-button" data-toggle="modal" data-target="#exampleModal-${i}">More Info!</button>

                            <div class="modal fade" id="exampleModal-${i}" data-backdrop="static" data-keyboard="false" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title" id="exampleModalLabel">${data.hits[i].recipe.label}</h5>
                                            <button id="btn-close-${i}" type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                                        </div>
                                        <div class="modal-body">
                                            <p><span style="color: red;">* Calories:</span> ${parseFloat(data.hits[i].recipe.calories).toFixed(2)} Kcal</p>
                                            <hr>
                                            <p class="parg fontt"><span style="color: red;">- Protein:</span> ${parseFloat(data.hits[i].recipe.digest[2].total).toFixed(2)} g</p>
                                            <p class="parg fontt"><span style="color: red;">- Fats:</span> ${parseFloat(data.hits[i].recipe.digest[0].total).toFixed(2)} g</p>
                                            <p class="fontt"><span style="color: red;">- Carbs:</span> ${parseFloat(data.hits[i].recipe.digest[1].total).toFixed(2)} g</p>
                                            <hr>
                                            <p class="parg fontt"><span style="color: red;">- Health Label(s):</span> ${health_label}</p>
                                            <p class="fontt"><span style="color: red;">- Diet Label:</span> ${diet_label}</p>
                                            <p class="fontt"><span style="color: red;">- Number of ingredients used:</span> ${data.hits[i].recipe.ingredients.length} Ingredients</p>
                                        </div>
                                        <div class="modal-footer">
                                            <a href="${data.hits[i].recipe.url}" class="btn btn-outline-info">Check Recipe!</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>`
            }
        }
    } else{
        var search = '<h1 class="alert alert-warning" style="text-align: center; margin-bottom: 30px">Results not found, try again.</h1>'
        _scroll = false
    }
    if(card_num == 12){
        document.querySelector('#recipe_search').classList.add('show');

        setTimeout(function() {
            $('.load-wrapper').fadeIn('slow', function(){
                $('.load-wrapper').fadeOut();
            });
            
            document.querySelector('#recipe_search').innerHTML = search;
        }, 2500);
        
        setTimeout(function() {
            document.querySelector('#recipe_search').classList.remove('show');
        }, 3000);

    } else{
        setTimeout(function() {
            $('.load-wrapper2').fadeIn('slow', function(){
                $('.load-wrapper2').fadeOut();
            });
            
            document.querySelector('#recipe_search').innerHTML = search;
        }, 2500);
    }

    setTimeout(function() {
        temp2 = document.querySelectorAll('#card-food');
        temp2.forEach(temp => {
            temp_func(temp);
        });
    }, 3000);

    if(_scroll == true){
        console.log(_scroll)
        if(filter == 'without-filter'){
            setTimeout(function() {
                window.onscroll = () => {
                    if(window.innerHeight + window.scrollY >= document.body.offsetHeight + 32 && _scroll == true) {
                        console.log('end of page without filter');

                        setTimeout(function() {
                            sendAPIrequest(card_num)
                        }, 500);
                    }
                }
            }, 3500);

        } else if(filter == 'with-filter'){
            setTimeout(function() {
                window.onscroll = () => {
                    if(window.innerHeight + window.scrollY >= document.body.offsetHeight + 32 && _scroll == true) {
                        console.log('end of page with filter');

                        setTimeout(function() {
                            SendAPIFilter(card_num)
                        }, 500);
                    }
                }
            }, 3500);
        }
    } else{
        console.log(_scroll)
    }

}


// This function is used for a bug fix, as when a modal is pressed, it lags out the webpage, and user is forced to reload.
// This is due to the animation of the card zoom-in interfering with the modal animation.
// This function removes the class causing the zoom-in animation, and re-adds it when user clicks off the modal, allowing for user-friendly experience.
function temp_func(temp){
    temp.addEventListener('click', () => {
        card_id = temp.getAttribute('data-id');
        var items = document.getElementsByClassName('cards');
        for (var i=0; i < items.length; i++) {
            items[i].id = 'removal';
          }

        document.querySelector(`#btn-close-${card_id}`).addEventListener('click', () => {
            setTimeout(function() {
                var items = document.getElementsByClassName('cards');
                for (var i=0; i < items.length; i++) {
                    items[i].id = 'card-recipe';
                }
            }, 500);
        })
    })
}