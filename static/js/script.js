$(document).ready(function() {
    load_results("false")
    $("#regrade").click(function(){
        load_results("true")
    });
});


var load_results = function(regrade){
    $('#example').DataTable( {
        "ajax": "/form-results?type="+appConfig.type+"&exam_id="+appConfig.exam_id+"&type_id="+appConfig.type_id+"&regrade="+regrade,
        "destroy": true,
        "columns": [
            {"data":"admno"},
            {"data":"name"},
            {"data":"eng"},
            {"data":"kisw"},
            {"data":"math"},
            {"data":"bio"},
            {"data":"chem"},
            {"data":"phy"},
            {"data":"hist"},
            {"data":"geo"},
            {"data":"cre"},
            {"data":"bus"},
            {"data":"comp"},
            {"data":"agr"},
            {"data":"frc"},
            {"data":"mus"},
            {"data":"ger"},
            {"data":"points"},
            {"data":"avg"},
            {"data":"grade"},
            {"data":"pos"},
        ],
        "order": [20, 'asc'],
        dom: 'Bfrtip',
        buttons: [
            'copyHtml5',
            'csvHtml5',
            {
                extend: 'excelHtml5',
                header: 'Kapsabet Boys High School'
            }
        ]
    });

}
