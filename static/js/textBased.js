function clickOption()
{
	document.getElementById("{{chc}}").checked = true;
}


function RunBtnClickEvent()
{
	//var opt=document.getElementById("opt").value;
	//var query=document.getElementById("DBquery").value;
	//alert(query);
	//document.getElementById("DBQoutput").value="RESULT\n"+query;
	
	if(document.getElementById("DBquery").value=="")
	{
		swal({
			title: "Empty Query",
			text: "Please enter (valid) query.",
			icon: "warning",
			button: "OK"
		});
		//alert("Please enter query");
		//return false;
	}
	else //if(document.getElementById("DBquery").value!="")
	{
		document.getElementById("initForm").submit();
	}
	//return false;
}

function ModifyPlaceHolder(element) 
{
	var data = 
	{
		ms: 'SELECT * FROM aisles;',
		bq: 'SELECT * FROM `cldsql.instacart.aisles`',
		md: '{"order_id": 1, "reordered": 1}'
	};
	var input = element.form.DBquery;
	input.placeholder = data[element.id];
}

$(document).ready(function () 
{
	$('#advTable').DataTable(
	{
		"order": []
	});
});