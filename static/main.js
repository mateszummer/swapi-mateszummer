function createTable(link='https://swapi.co/api/planets') {
    $('.main-gears').addClass("fa-spin")
    $('.main-gears').show()
    fetch(link)
    .then((resp) => resp.json())
    .then(function(data) {
        $('.tr_class').remove()
        for (i = 0; i < data.results.length; i++) {
            let row = `<tr class="tr_class">
                            <td>${data.results[i]['name']}</td>
                            <td>${data.results[i]['diameter']}</td>
                            <td>${data.results[i]['climate']}</td>
                            <td>${data.results[i]['terrain']}</td>
                            <td>${data.results[i]['surface_water']} </td>
                            <td>${data.results[i]['population']} </td>
                            <td id="residents_${i}"></td>
                        </tr>`
            document.getElementById("table").insertAdjacentHTML('beforeend', row);
            $('tr_class').hide()
            if (i == data.results.length -1) {
                $('tr_class').show()
                $('.main-gears').removeClass("fa-spin")
                $('.main-gears').hide()

            }
            setResidents(data, i);
        };
        setButtons(data);
    });
}

function setResidents(data, i) {
    if (data.results[i]["residents"].length == 0) {
        document.getElementById(`residents_${i}`).innerHTML = "No known residents";
    }
    else {
        let count = data.results[i]['residents'].length
        document.getElementById(`residents_${i}`).innerHTML = `
            <button class="btn btn-outline-info" type="button" id='residents_${i}_button' data-toggle="modal" data-target="#residents_${i}_modal"> ${count} resident(s)</button>
            <div id="residents_${i}_modal" class="modal fade" role="dialog">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                        <h4 class="modal-title">Residents of ${data.results[i]['name']}
                        <i class="fa fa-cog gears" style="font-size:30px"></i></h4>
                            </div>
                            <div id="residents_${i}_modal_body" class="modal-body">
                            </div>
                        <div class="modal-footer">
                        <button type="button" class="btn btn-outline-primary" data-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>`
        document.getElementById(`residents_${i}_button`).addEventListener('click', function () {
            $('.gears').addClass("fa-spin")
            $('.gears').show()
            createResidentsTable(data, i)
        });
    }
}

function createResidentsTable(data, i) {
    let residents = []
    document.getElementById(`residents_${i}_modal_body`).innerHTML = `
    <table class="table table-bordered" id="residents_${i}_table">
        <tr>
            <th>Name</th>
            <th>Height</th>
            <th>Mass</th>
            <th>Hair color</th>
            <th>Skin color</th>
            <th>Eye color</th>
            <th>Birth year</th>
            <th>Gender</th>
        </tr>
    </table>`
    let counter = 0
    for (let j of data.results[i].residents) {
        fetch(j)
        .then((resp) => resp.json())
        .then(function(resident) {
            let row = `<tr class="tr_residents">
                            <td>${resident['name']}</td>
                            <td>${resident['height']}</td>
                            <td>${resident['mass']}</td>
                            <td>${resident['hair_color']}</td>
                            <td>${resident['skin_color']}</td>
                            <td>${resident['eye_color']}</td>
                            <td>${resident['birth_year']}</td>
                            <td>${resident['gender']}</td>
                        </tr>`
            document.getElementById(`residents_${i}_table`).insertAdjacentHTML('beforeend', row);
            $(".tr_residents").hide()
            if (counter == data.results[i].residents.length-1) {
                $(".tr_residents").show();
                $(".gears").removeClass("fa-spin");
                $('.gears').hide()

            }
            counter +=1
        })
    }

}

function setButtons(data) {
    document.getElementById("buttons").innerHTML = `<button id="btn_previous" class="btn-primary">Previous</button>
                                                    <button id="btn_next" class="btn-primary">Next</button>`
    if (data.previous == null) {
        document.getElementById("btn_previous").disabled = true;
        document.getElementById("btn_previous").className = "btn-default"
    }
    if (data.next == null) {
        document.getElementById("btn_next").disabled = true;
        document.getElementById("btn_next").className = "btn-default"
    }
    document.getElementById("btn_previous").addEventListener('click', function(){
        let link = data.previous;
        createTable(link);
    });
    document.getElementById("btn_next").addEventListener('click', function(){
        let link = data.next;
        createTable(link);
    });
}

createTable()
