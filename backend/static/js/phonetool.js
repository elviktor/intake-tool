// TO DO:
// 1) Add wrongful termination entries to dictionary to flesh out system
// 2) Clean up display with CSS
// 3) Experiment with additional fields and features
//    ex.) url's, embedded video, maps, iframes with 3rd party resources, etc...
// 4) Create Django database to generate script and dictionary
// 5) Think about how to use keywords to establish links between services

// Create dictionary and usage counter for exporting usage data
var usage_df = {};
var usage_id = 0; // Usage id must be unique for each use. I can use datetime for this.

var test_df = {};

// Load JSON dataframes
var m_df = JSON.parse(moves);
var mdict_df = JSON.parse(definitions);

// Moves Dataframe (m_df) index list
// the list items follow the column names of m_df
var idx = ["m0", "m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9", "m10"];

// Declare move state (ms) and move state list (ms_list)
var ms = 0;
var ms_list = ["g_greet"];
console.log("Greetings!");

var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

// greet_quote
var settings = {
  url: "https://justiceseed.com/intake/api/moves",
  method: "POST",
  timeout: 0,
  headers: {
    "Content-Type": "application/x-www-form-urlencoded",
    Accept: "application/json"
  },
  data: {
    csrfmiddlewaretoken: csrftoken,
    move_name: "Greet"
  }
};

$.ajax(settings).done(function(response) {
  document.getElementById("text").innerHTML = response.quote;
});

// **FOR TESTING: Initialize ms and ms_list values
//var ms = 3;
//var ms_list = ['g_greet', 't_triage', 'i_facing_eviction', 'q_have_petition', 'r_leave_home'];
// # ***********************************************

function clear_fields() {
  document.getElementById("info").innerHTML = "";
  document.getElementById("link").innerHTML = "";
}

function response_button(id) {
  clear_fields();
  console.log("Response button ms status: " + ms);
  // Get selected response move from innerText of response button
  var __future_move = document.getElementById(id).innerText;

  // Convert Move title to name readable by database
  // Example: r_come_to_court > come to court
  function get_suffix(str) {
    var regex = /^[a-z]\w([a-z]\w+)/;
    var suffix = str.match(regex);
    var suffix_prep = suffix[1].replace(/_/g, " ");

    return suffix_prep;
  }

  var future_move = get_suffix(__future_move);

  // Display response instructions
  console.log("Instructions for response: " + future_move);
  console.log("response_button ms_list: " + ms_list);

  // future_move_quote
  var settings = {
    url: "https://justiceseed.com/intake/api/moves",
    method: "POST",
    timeout: 0,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Accept: "application/json"
    },
    data: {
      csrfmiddlewaretoken: csrftoken,
      move_name: future_move
    }
  };

  $.ajax(settings).done(function(response) {
    //console.log(response.quote);
    document.getElementById("text").innerHTML = response.info;
    //if (response.info != "") {
    //document.getElementById('info').innerHTML = "Information: " + response.info;
    //}
    if (response.link != "") {
      document.getElementById("link").href = response.link;
      document.getElementById("link").innerHTML = response.link;
    }
  });

  // Check if this response requires emergency treatment.
  emergency_checker(future_move);

  // Advance ms and ms_list
  ms_list.push(__future_move);
  console.log("response button ms_list: " + ms_list);
  ms += 1;
  console.log("ms = " + ms);

  // Clear unused response buttons
  // **Code the response CLASS of buttons to 'display=None'
  //    when they are empty.
  var responses = document.querySelectorAll(".response");
  for (var i = 0; i < responses.length; i++) {
    responses[i].innerHTML = "";
    responses[i].style.display = "none";
  }

  // Reveal NEXT button
  document.getElementById("next_button").innerHTML = "Next";
  document.getElementById("next_button").style.display = "block";
}

function issue_button(id) {
  clear_fields();
  console.log("Issue button ms status: " + ms);
  // Get selected response move from innerText of response button
  var __future_move = document.getElementById(id).innerText;
  console.log("this is id " + id);
  // Display response instructions
  console.log("Description of issue (ON MOUSEOVER)");

  // Convert Move title to name readable by database
  // Example: r_come_to_court > come to court
  function get_suffix(str) {
    var regex = /^[a-z]\w([a-z]\w+)/;
    var suffix = str.match(regex);
    var suffix_prep = suffix[1].replace(/_/g, " ");

    return suffix_prep;
  }

  var future_move = get_suffix(__future_move);

  // Display response instructions
  console.log("Instructions for response: " + future_move);

  // future_move_quote
  var settings = {
    url: "https://justiceseed.com/intake/api/moves",
    method: "POST",
    timeout: 0,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Accept: "application/json"
    },
    data: {
      csrfmiddlewaretoken: csrftoken,
      move_name: future_move
    }
  };

  $.ajax(settings).done(function(response) {
    //console.log(response.quote);
    document.getElementById("text").innerHTML =
      "Description of issue: " + response.info;
  });

  // Advance ms and ms_list
  ms_list.push(__future_move);
  ms += 1;
  console.log("ms = " + ms);
  console.log(ms_list);
  console.log("issue button future_move: " + __future_move);

  // Toggle visibility of issue menu and next button
  document.getElementById("issue_menu_container").style.display = "none";
  document.getElementById("next_button").innerHTML = "Next";
  document.getElementById("next_button").style.display = "block";
}

function build_issue_buttons() {
  clear_fields();
  // Step 1
  //-------
  $.get("https://justiceseed.com/intake/api/sequences", function(data, status) {
    // Create object of scripts to assist in navigating Sequence API data
    var script_list = [];
    var script_dict = {};

    // Create script_list
    // (This will help to organize the script data)
    for (var i = 0; i < data["sequences"].length; i++) {
      if (script_list.includes(data["sequences"][i]["script"]) == false) {
        script_list.push(data["sequences"][i]["script"]);
      }
    }

    // Generate object keys for script_dict from script_list
    // (This will help to organize the script data)
    for (var i = 0; i < script_list.length; i++) {
      script_dict[script_list[i]] = {};
    }

    // Populate Script dictiionary lists by cycling through all
    // sequence data by script_list titles
    for (var j = 0; j < script_list.length; j++) {
      var script_move_list = [];
      // Cycle through the moves in a script
      for (var i = 0; i < data["sequences"].length; i++) {
        if (data["sequences"][i]["script"] == script_list[j]) {
          script_move_list.push(data["sequences"][i]["move"]);
        }
        script_dict[script_list[j]] = script_move_list;
      }
    }

    // Declare past, present and future move data
    var script_dict_keys = Object.keys(script_dict);

    const regex = /^([a-z])/;
    var issue_list = [];
    for (var i = 0; i < script_dict_keys.length; i++) {
      // Make sure that the present move is Triage prefix (t)
      // and the future move is Issue prefix (t)
      var __triage_prefix = script_dict[script_dict_keys[i]][ms].match(regex);
      var __issue_prefix = script_dict[script_dict_keys[i]][ms + 1].match(
        regex
      );
      var triage_prefix = __triage_prefix[1];
      var issue_prefix = __issue_prefix[1];
      console.log("This is triage_prefix: " + triage_prefix);
      console.log("This is issue_prefix: " + issue_prefix);
      if (triage_prefix == "t" && issue_prefix == "i") {
        // Save unique issues to issue_list
        if (i == 0) {
          issue_list.push(script_dict[script_dict_keys[i]][ms + 1]);
        } else {
          if (
            issue_list.includes(script_dict[script_dict_keys[i]][ms + 1]) ==
            false
          ) {
            issue_list.push(script_dict[script_dict_keys[i]][ms + 1]);
          }
        }
      }
    }

    // Convert Move title to name readable by database
    // Example: r_come_to_court > come to court
    function get_suffix(str) {
      var regex = /^[a-z]\w([a-z]\w+)/;
      var suffix = str.match(regex);
      var suffix_prep = suffix[1].replace(/_/g, " ");

      return suffix_prep;
    }

    // Convert all future2 moves
    var issue_api_title_list = [];
    for (var i = 0; i < issue_list.length; i++) {
      issue_api_title_list.push(get_suffix(issue_list[i]));
    }

    console.log(issue_api_title_list);

    // Traverse list of issues and create button labels from it.
    for (var j = 0; j < issue_list.length; j++) {
      var button_id = "issue_" + j;
      var info_id = "issue_" + j + "_info";
      var button = document.getElementById(button_id);
      var button_info = document.getElementById(info_id);

      // Write button reference name to hidden button_info entity
      button_info.innerHTML = issue_list[j];

      // future2_move_quote
      var settings = {
        url: "https://justiceseed.com/intake/api/moves",
        method: "POST",
        timeout: 0,
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          Accept: "application/json"
        },
        data: {
          csrfmiddlewaretoken: csrftoken,
          move_name: issue_api_title_list[j]
        }
      };

      if (j == 0) {
        $.ajax(settings).done(function(response) {
          // Display called API Move quote data
          document.getElementById("issue_0").innerText = response.quote;
        });

        // Write label to visible button entity
        button.style.display = "inline";
      }
      if (j == 1) {
        $.ajax(settings).done(function(response) {
          // Display called API Move quote data
          document.getElementById("issue_1").innerText = response.quote;
        });

        // Write label to visible button entity
        button.style.display = "inline";
      }
      if (j == 2) {
        $.ajax(settings).done(function(response) {
          // Display called API Move quote data
          document.getElementById("issue_2").innerText = response.quote;
        });

        // Write label to visible button entity
        button.style.display = "inline";
      }
      if (j == 3) {
        $.ajax(settings).done(function(response) {
          // Display called API Move quote data
          document.getElementById("issue_3").innerText = response.quote;
        });

        // Write label to visible button entity
        button.style.display = "inline";
      }
      if (j == 4) {
        $.ajax(settings).done(function(response) {
          // Display called API Move quote data
          document.getElementById("issue_4").innerText = response.quote;
        });

        // Write label to visible button entity
        button.style.display = "inline";
      }
      if (j == 5) {
        $.ajax(settings).done(function(response) {
          // Display called API Move quote data
          document.getElementById("issue_5").innerText = response.quote;
        });

        // Write label to visible button entity
        button.style.display = "inline";
      }
      if (j == 6) {
        $.ajax(settings).done(function(response) {
          // Display called API Move quote data
          document.getElementById("issue_6").innerText = response.quote;
        });

        // Write label to visible button entity
        button.style.display = "inline";
      }
      if (j == 7) {
        $.ajax(settings).done(function(response) {
          // Display called API Move quote data
          document.getElementById("issue_7").innerText = response.quote;
        });

        // Write label to visible button entity
        button.style.display = "inline";
      }
      if (j == 8) {
        $.ajax(settings).done(function(response) {
          // Display called API Move quote data
          document.getElementById("issue_8").innerText = response.quote;
        });

        // Write label to visible button entity
        button.style.display = "inline";
      }
      if (j == 9) {
        $.ajax(settings).done(function(response) {
          // Display called API Move quote data
          document.getElementById("issue_9").innerText = response.quote;
        });

        // Write label to visible button entity
        button.style.display = "inline";
      }
      if (j == 10) {
        $.ajax(settings).done(function(response) {
          // Display called API Move quote data
          document.getElementById("issue_10").innerText = response.quote;
        });

        // Write label to visible button entity
        button.style.display = "inline";
      }

      $.ajax(settings).done(function(response) {
        // Display called API Move quote data
        button.innerText = response.quote;
      });

      // Write label to visible button entity
      button.style.display = "inline";
    }
  });
}

function emergency_checker(move) {
  // UPDATE!!!!!
  // Check if move is marked as an emergency.
  // If so then reveal emergency window with instructions.

  // future2_move_quote
  var settings = {
    url: "https://justiceseed.com/intake/api/moves",
    method: "POST",
    timeout: 0,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Accept: "application/json"
    },
    data: {
      csrfmiddlewaretoken: csrftoken,
      move_name: move
    }
  };

  $.ajax(settings).done(function(response) {
    // Display called API Move quote data
    if (response.emergency == "y") {
      var emergency_def = response.info;
      document.getElementById("emergency_container").style.display = "block";
      document.getElementById("emergency_text").innerText = emergency_def;
    }
  });
}

function action_button() {
  clear_fields();
  //=================================
  // Next Move Algorithm
  //=================================
  // Use the following algorithm to check m_df to decide which next moves to display.
  //---------------------------------
  console.log("Action button ms status: " + ms);
  // Clear emergency field
  document.getElementById("emergency_container").style.display = "none";

  // Check if ms > 0 (otherwise looking for past step will be out of range
  // when looking at past moves.
  if (ms > 0 && ms < 99) {
    var past_query_list = [ms_list[ms - 1], ms_list[ms]];

    // Step 1
    //-------
    $.get("https://justiceseed.com/intake/api/sequences", function(
      data,
      status
    ) {
      // Create object of scripts to assist in navigating Sequence API data
      var script_list = [];
      var script_dict = {};

      // Create script_list
      // (This will help to organize the script data)
      for (var i = 0; i < data["sequences"].length; i++) {
        if (script_list.includes(data["sequences"][i]["script"]) == false) {
          script_list.push(data["sequences"][i]["script"]);
        }
      }

      // Generate object keys for script_dict from script_list
      // (This will help to organize the script data)
      for (var i = 0; i < script_list.length; i++) {
        script_dict[script_list[i]] = {};
      }

      // Populate Script dictiionary lists by cycling through all
      // sequence data by script_list titles
      for (var j = 0; j < script_list.length; j++) {
        var script_move_list = [];
        // Cycle through the moves in a script
        for (var i = 0; i < data["sequences"].length; i++) {
          if (data["sequences"][i]["script"] == script_list[j]) {
            script_move_list.push(data["sequences"][i]["move"]);
          }
          script_dict[script_list[j]] = script_move_list;
        }
      }

      // Declare past, present and future move data
      var script_dict_keys = Object.keys(script_dict);

      var past_move;
      var present_move;
      var future_move;
      var future2_move_list = [];

      for (var i = 0; i < script_dict_keys.length; i++) {
        if (
          script_dict[script_dict_keys[i]][ms - 2] == ms_list[ms - 2] &&
          script_dict[script_dict_keys[i]][ms - 1] == ms_list[ms - 1] &&
          script_dict[script_dict_keys[i]][ms] == ms_list[ms]
        ) {
          past_move = script_dict[script_list[i]][ms - 1];
          present_move = script_dict[script_list[i]][ms];
          future_move = script_dict[script_list[i]][ms + 1];

          // Create list of future2_moves to fill question responses options
          future2_move_list.push(script_dict[script_list[i]][ms + 2]);

          console.log("All is good. This is future move:" + present_move);
        }
      }

      // Convert Move title to name readable by database
      // Example: r_come_to_court > come to court
      function get_suffix(str) {
        var regex = /^[a-z]\w([a-z]\w+)/;
        var suffix = str.match(regex);
        var suffix_prep = suffix[1].replace(/_/g, " ");

        return suffix_prep;
      }

      var past_move_api_title = get_suffix(past_move);
      var present_move_api_title = get_suffix(present_move);
      var future_move_api_title = get_suffix(future_move);

      // Convert all future2 moves
      var future2_move_api_title_list = [];
      if (future2_move_list[0] != null) {
        for (var i = 0; i < future2_move_list.length; i++) {
          future2_move_api_title_list.push(get_suffix(future2_move_list[i]));
        }
      }

      //console.log(future2_move_api_title_list);

      // Step 2
      //-------
      // Check move prefix to trigger different algorithm and display behaviors.
      // Prefixes: questions (q), triage (t), greeting (g), reply (r), conclusion (c)
      //           intake info (p)

      // Store future prefix
      // For example: q_what_time_is_it (q)
      const regex = /^([a-z])/;
      var __future_prefix = future_move.match(regex);
      var future_prefix = __future_prefix[1];

      document.getElementById("future_prefix").innerText = future_prefix;
      console.log("This is future prefix: " + future_prefix);

      // # (Prefix 1) Questions (q)
      // If the future (ms+1) move has a 'q' prefix then
      // Store the future2 (ms+2) moves as optional answers to display

      if (future_prefix == "q") {
        // QUESTION display
        console.log("Question: " + future_move);

        // future_move_quote
        var settings = {
          url: "https://justiceseed.com/intake/api/moves",
          method: "POST",
          timeout: 0,
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            Accept: "application/json"
          },
          data: {
            csrfmiddlewaretoken: csrftoken,
            move_name: future_move_api_title
          }
        };

        $.ajax(settings).done(function(response) {
          //console.log(response.quote);
          document.getElementById("text").innerText = response.quote;
        });

        // ANSWER CHOICE display
        var answer_list = [];
        for (var i = 0; i < future2_move_api_title_list.length; i++) {
          if (i == 0) {
            answer_list.push(future2_move_api_title_list[i]);

            console.log("Choice: " + future2_move_api_title_list[i]);
            var id = "response_" + String(i);
            var info_id = "response_" + String(i) + "_info";
            console.log(id);

            // future2_move_quote
            var settings = {
              url: "https://justiceseed.com/intake/api/moves",
              method: "POST",
              timeout: 0,
              headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                Accept: "application/json"
              },
              data: {
                csrfmiddlewaretoken: csrftoken,
                move_name: future2_move_api_title_list[i]
              }
            };

            $.ajax(settings).done(function(response) {
              // Display called API Move quote data
              document.getElementById("response_0").innerText = response.quote;
              console.log(response.quote);
            });

            document.getElementById(info_id).innerText = future2_move_list[i];
            // Reveal question responses
            document.getElementById(id).style.display = "inline";
          } else if (answer_list.includes(future2_move_list[i]) == false) {
            answer_list.push(future2_move_list[i]);

            console.log("Choice: " + future2_move_api_title_list[i]);
            var id = "response_" + String(i);
            var info_id = "response_" + String(i) + "_info";
            console.log(id);

            // future2_move_quote
            var settings = {
              url: "https://justiceseed.com/intake/api/moves",
              method: "POST",
              timeout: 0,
              headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                Accept: "application/json"
              },
              data: {
                csrfmiddlewaretoken: csrftoken,
                move_name: future2_move_api_title_list[i]
              }
            };

            if (i == 0) {
              $.ajax(settings).done(function(response) {
                // Display called API Move quote data
                document.getElementById("response_0").innerText =
                  response.quote;
              });
              document.getElementById("response_0_info").innerText =
                future2_move_list[i];
              // Reveal question responses
              document.getElementById("response_0").style.display = "inline";
            }
            if (i == 1) {
              $.ajax(settings).done(function(response) {
                // Display called API Move quote data
                document.getElementById("response_1").innerText =
                  response.quote;
              });
              document.getElementById("response_1_info").innerText =
                future2_move_list[i];
              // Reveal question responses
              document.getElementById("response_1").style.display = "inline";
            }
            if (i == 2) {
              $.ajax(settings).done(function(response) {
                // Display called API Move quote data
                document.getElementById("response_2").innerText =
                  response.quote;
              });
              document.getElementById("response_2_info").innerText =
                future2_move_list[i];
              // Reveal question responses
              document.getElementById("response_2").style.display = "inline";
            }
            if (i == 3) {
              $.ajax(settings).done(function(response) {
                // Display called API Move quote data
                document.getElementById("response_3").innerText =
                  response.quote;
              });
              document.getElementById("response_3_info").innerText =
                future2_move_list[i];
              // Reveal question responses
              document.getElementById("response_3").style.display = "inline";
            }
            if (i == 4) {
              $.ajax(settings).done(function(response) {
                // Display called API Move quote data
                document.getElementById("response_4").innerText =
                  response.quote;
              });
              document.getElementById("response_4_info").innerText =
                future2_move_list[i];
              // Reveal question responses
              document.getElementById("response_4").style.display = "inline";
            }
            if (i == 5) {
              $.ajax(settings).done(function(response) {
                // Display called API Move quote data
                document.getElementById("response_5").innerText =
                  response.quote;
              });
              document.getElementById("response_5_info").innerText =
                future2_move_list[i];
              // Reveal question responses
              document.getElementById("response_5").style.display = "inline";
            }
            if (i > 5) {
              $.ajax(settings).done(function(response) {
                // Display called API Move quote data
                document.getElementById(id).innerText = response.quote;
              });
              document.getElementById(info_id).innerText = future2_move_list[i];
              // Reveal question responses
              document.getElementById(id).style.display = "inline";
            }
          }
        }

        document.getElementById("next_button").innerHTML = "";
        document.getElementById("next_button").style.display = "none";

        // Advance move state (ms) << For questions this is triggered when a response button is pressed
        ms += 1;
        ms_list.push(future_move);
        console.log("ms = " + ms);
      }

      // # (Prefix 2) Conclusions (c)
      // 1) Reset the list and counter
      // 2) Display closing message
      // 3) Review/report emergency keywords
      // 4) *Store completed move_list to web database via POST
      if (future_prefix == "c") {
        // Conclusion display
        console.log("Conclusion: " + future_move);

        // future_move_quote
        var settings = {
          url: "https://justiceseed.com/intake/api/moves",
          method: "POST",
          timeout: 0,
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            Accept: "application/json"
          },
          data: {
            csrfmiddlewaretoken: csrftoken,
            move_name: future_move_api_title
          }
        };

        $.ajax(settings).done(function(response) {
          document.getElementById("text").innerHTML = response.quote;
          if (response.info != "") {
            document.getElementById("info").innerHTML =
              "Information: " + response.info;
          }
          if (response.link != "") {
            document.getElementById("link").href = response.link;
            document.getElementById("link").innerHTML = response.link;
          }
        });

        // Advance move state (ms) << For questions this is triggered when a response button is pressed
        ms += 1;
        ms_list.push(future_move);
        console.log("ms = " + ms);

        // Export usage data <<<<<<< Use AJAX POST Function*************
        usage_df[usage_id] = {};
        usage_df[usage_id] = ms_list;
        usage_id += 1; // Again, I will use datetime library to make this number unique
        console.log("EXPORT!");
        console.log(usage_df);

        var ex_obj = {
          m1: "",
          m2: "",
          m3: "",
          m4: "",
          m5: "",
          m6: "",
          m7: "",
          m8: "",
          m9: "",
          m10: "",
          m11: "",
          m12: "",
          m13: "",
          m14: "",
          m15: "",
          m16: "",
          m17: "",
          m18: "",
          m19: "",
          m20: ""
        };

        for (var i = 0; i < ms_list.length; i++) {
          var c = i + 1;
          ex_obj["m" + c] = ms_list[i];
        }

        var settings = {
          url: "https://justiceseed.com/intake/api/sequencerecords",
          method: "POST",
          timeout: 0,
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            Accept: "application/json"
          },
          data: {
            csrfmiddlewaretoken: csrftoken,
            m1: ex_obj.m1,
            m2: ex_obj.m2,
            m3: ex_obj.m3,
            m4: ex_obj.m4,
            m5: ex_obj.m5,
            m6: ex_obj.m6,
            m7: ex_obj.m7,
            m8: ex_obj.m8,
            m9: ex_obj.m9,
            m10: ex_obj.m10,
            m11: ex_obj.m11,
            m12: ex_obj.m12,
            m13: ex_obj.m13,
            m14: ex_obj.m14,
            m15: ex_obj.m15,
            m16: ex_obj.m16,
            m17: ex_obj.m17,
            m18: ex_obj.m18,
            m19: ex_obj.m19,
            m20: ex_obj.m20
          }
        };

        $.ajax(settings).done(function(response) {
          console.log(response);
        });

        // Reset move state (ms) to 999 < a special ms number ONLY for RESET screen
        ms = 999;
        ms_list = []; // << POST ms_list to database to help collect user data
        console.log("ms = " + ms);

        //DISPLAY optional reset message.
        document.getElementById("next_button").innerHTML = "Reset";
      }

      // # (Prefix 3) Triage (t)
      if (future_prefix == "t") {
        // Toggle visibility of issue menu and next button
        document.getElementById('issue_menu_container"').style.display =
          "block";
        document.getElementById("next_button").innerHTML = "";
        document.getElementById("next_button").style.display = "none";

        // QUESTION display
        console.log("Instruction: " + future_move);

        // future_move_quote
        var settings = {
          url: "https://justiceseed.com/intake/api/moves",
          method: "POST",
          timeout: 0,
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            Accept: "application/json"
          },
          data: {
            csrfmiddlewaretoken: csrftoken,
            move_name: future_move_api_title
          }
        };

        $.ajax(settings).done(function(response) {
          document.getElementById("text").innerHTML = response.quote;
          if (response.info != "") {
            document.getElementById("info").innerHTML =
              "Information: " + response.info;
          }
          if (response.link != "") {
            document.getElementById("link").href = response.link;
            document.getElementById("link").innerHTML = response.link;
          }
        });

        // Advance move state (ms) << For questions this is triggered when a response button is pressed
        ms += 1;
        ms_list.push(future_move);
        console.log("ms = " + ms);
      }
    });
  }

  // For initial move state - Greeting (g)
  else if (ms == 999) {
    // Advance move state (ms)
    ms = 0;
    ms_list.push("g_greet");
    console.log("ms = " + ms);

    //DISPLAY greeting message.
    console.log("Greetings!");

    // greet_quote
    var settings = {
      url: "https://justiceseed.com/intake/api/moves",
      method: "POST",
      timeout: 0,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Accept: "application/json"
      },
      data: {
        csrfmiddlewaretoken: csrftoken,
        move_name: "Greet"
      }
    };

    $.ajax(settings).done(function(response) {
      document.getElementById("text").innerHTML = response.quote;
    });

    document.getElementById("next_button").innerHTML = "Next";
  }

  // For initial move state - Greeting (g)
  else if (ms == 0) {
    // Advance move state (ms)
    ms += 1;
    ms_list.push("t_triage");
    console.log("ms = " + ms);

    //DISPLAY triage message.
    console.log("Triage!");

    // triage_quote
    var settings = {
      url: "https://justiceseed.com/intake/api/moves",
      method: "POST",
      timeout: 0,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Accept: "application/json"
      },
      data: {
        csrfmiddlewaretoken: csrftoken,
        move_name: "Triage"
      }
    };

    $.ajax(settings).done(function(response) {
      document.getElementById("text").innerHTML = response.quote;
      if (response.info != "") {
        document.getElementById("info").innerHTML =
          "Information: " + response.info;
      }
      if (response.link != "") {
        document.getElementById("link").href = response.link;
        document.getElementById("link").innerHTML = response.link;
      }
    });

    // Toggle visibility of issue menu and next button
    document.getElementById("issue_menu_container").style.display = "block";
    document.getElementById("next_button").innerHTML = "";
    document.getElementById("next_button").style.display = "none";

    // Add issue text to menu
    build_issue_buttons();
  }
}
