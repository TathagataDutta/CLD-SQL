function check_value(fieldvalue)
{    
    switch(fieldvalue)
    {
        case 1:

            document.getElementById("imagedest").innerHTML = "<img src='static/images/MySQL_ERD.png'>";
                break;

        case 2:

            document.getElementById("imagedest").innerHTML = "<img src='static/images/MySQL_ERD_Schema.png'>";
                break;

        case 3:

            document.getElementById("imagedest").innerHTML = "<img src='static/images/BigQuery_Schema.png'>"; 
                break;

        case 4:

            document.getElementById("imagedest").innerHTML = "<img src='static/images/MongoDB_Schema.png'>"; 
                break;
    }
}