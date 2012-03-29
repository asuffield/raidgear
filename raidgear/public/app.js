$(function() {
    if (typeof character_name != "undefined") {
      setupForm();
    }

    if (typeof free_characters != "undefined") {
      setupPlanner();
    }
});

function setupForm() {
  $('.equip_select').change(function(event) {
      var name = $(this).attr('name');
      var value = $(this).val();

      $.post('/character/' + character_name + '/equip', 
             {slot: name.replace('equip_', ''), gear: value},
             function(data) { $('#advice').html(data) }
             );
    });

  $('.autopost').change(function(event) {
      var name = $(this).attr('name');
      var value = $(this).val();

      $.post('/character/' + character_name + '/' + name,
             {value: value},
             function(data) { if (data) { $('#advice').html(data) } }
             );
    });

  spec = $('#spec');
  function updateSpecStyle(event) {
    option = spec.find('option:selected');
    if (option.length) {
      spec.css('backgroundColor', option.css('backgroundColor'));
      spec.css('color', option.css('color'));
    }
  }
  if (spec) {
    spec.change(updateSpecStyle);
    updateSpecStyle();
  }
}

function setupPlanner() {
  var group_template = $('.group.template');
  var player_slot_template = $('.player_slot.template');
  var next_group = 1;

  var total_characters = free_characters.length;
  $.each(groups, function(i, group) {
      total_characters += group.members.length;
    });

  var make_character = function(c) {
    var slot = player_slot_template.clone().removeClass('template').addClass(c.spec);
    slot.find('.name').text(c.name);
    slot.find('.score').text(c.score.toPrecision(3));
    slot.find('.advclass').text(c.advclass);
    slot.data('score', c.score);
    slot.data('spec', c.spec);
    return slot;
  };

  var ready_players = $('.ready_players');
  $.each(free_characters, function(i, c) {
      make_character(c).appendTo(ready_players);
    });

  var update_group = function(group) {
    var players = group.find('.player_slot');
    var players_label = group.find('.players');

    players_label.text(players.length + '/' + group.data('size'));

    scores = {melee: 0, ranged: 0, healing: 0, tank: 0};
    players.each(function(i, slot) {
        scores[$(slot).data('spec')] += $(slot).data('score');
      });
    scores.damage = scores.melee + scores.ranged;
    for (spec in scores) {
      group.find('.score.' + spec).text(scores[spec].toPrecision(3));
    }
  };

  var change_mode = function (event) {
    var group = $(this).parents('.group');
    var size = parseInt(group.find('.mode').val());
    group.data('size', size);
    update_group(group);
  };

  var group_receive = function(event, ui) {
    var group = $(this).parents('.group');
    var items = $(this).find('.player_slot').length;
    var size = group.data('size');
    if (items > size) {
      $(ui.sender).sortable('cancel');
    }
    else {
      update_group(group);
    }
  };

  var group_stop = function(event, ui) {
    var group = $(this).parents('.group');
    update_group(group);
  };

  var setup_player_box = function(box) {
    box.disableSelection().sortable({tolerance: 'pointer', revert: 100, receive: group_receive, stop: group_stop});
    $('.player_box').sortable('option', 'connectWith', '.player_box');
  };

  var remove_group = function() {
    var group = $(this).parents('.group');
    group.find('.player_slot').each(function(i, slot) {
        $(slot).detach().appendTo(ready_players);
      });
    group.remove();
  };

  var add_group = function() {
    var group_id = next_group++;
    new_group = group_template.clone()
      .attr('id', 'group_' + group_id)
      .insertBefore('#add_group')
      .removeClass('template');

    new_group.data('size', 0);

    new_group.find('.remove_group').click(remove_group);
    new_group.find('select.mode').change(change_mode);
    setup_player_box(new_group.find('.player_box'));
    update_group(new_group);
  };

  setup_player_box(ready_players);
  $('#add_group').click(add_group);
}
