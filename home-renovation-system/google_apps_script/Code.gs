/**
 * Novality Store — Home Renovation Management System
 * Google Sheets companion script.
 *
 * Install
 *   1. Upload the .xlsx and open it with Google Sheets (File → Save as Google Sheets).
 *   2. Extensions → Apps Script.
 *   3. Replace the default file with this script. Save.
 *   4. Reload the spreadsheet. Use the "Novality Store" menu.
 *
 * Brand
 *   Primary #16352F  ·  Sand #E8DDCB  ·  Terracotta #C86B4A  ·  Ivory #F8F6F1
 */

var BRAND = {
  primary: '#16352F',
  sand: '#E8DDCB',
  terracotta: '#C86B4A',
  ivory: '#F8F6F1',
  sage: '#719B7A',
  amber: '#D99A3D',
  danger: '#C75C5C',
};

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Novality Store')
    .addItem('Open homeowner dashboard', 'goDashboard')
    .addItem('Open module hub', 'goModuleHub')
    .addSeparator()
    .addItem('Add expense…', 'addExpense')
    .addItem('Add task…', 'addTask')
    .addItem('Add material…', 'addMaterial')
    .addItem('Log a message…', 'addMessage')
    .addSeparator()
    .addItem('Refresh shopping list', 'refreshShoppingList')
    .addItem('Highlight overdue tasks', 'highlightOverdue')
    .addItem('Build this-week calendar view', 'thisWeekAgenda')
    .addSeparator()
    .addItem('Email maintenance reminders', 'emailMaintenanceReminders')
    .addItem('Email unread messages digest', 'emailUnreadDigest')
    .addSeparator()
    .addItem('About this system', 'showAbout')
    .addToUi();
}

function goDashboard() {
  var ss = SpreadsheetApp.getActive();
  var sh = ss.getSheetByName('Dashboard');
  if (sh) ss.setActiveSheet(sh);
}

function showAbout() {
  var html = HtmlService.createHtmlOutput(
    '<div style="font-family:Georgia,serif;color:#202522;background:#F8F6F1;padding:16px">' +
      '<h2 style="color:#16352F;margin:0 0 8px">Novality Store</h2>' +
      '<p style="margin:0 0 12px">Home Renovation Management System — a digital twin of the home.</p>' +
      '<p>Every room, material, contractor, expense, document, task, photo, warranty and ' +
      'maintenance activity is connected to a place in the house.</p>' +
      '<p style="color:#C86B4A"><b>Tip:</b> change <i>Settings → Active Project ID</i> to switch dashboards.</p>' +
      '</div>'
  )
    .setWidth(420)
    .setHeight(260);
  SpreadsheetApp.getUi().showModalDialog(html, 'About');
}

function setting_(key) {
  var sh = SpreadsheetApp.getActive().getSheetByName('Settings');
  if (!sh) return '';
  var values = sh.getRange(5, 1, 40, 2).getValues();
  for (var i = 0; i < values.length; i++) {
    if (String(values[i][0]) === key) return values[i][1];
  }
  return '';
}

function activeProject_() {
  return String(setting_('Active Project ID') || 'PRJ-001');
}

function nextId_(sheetName, prefix, col) {
  var sh = SpreadsheetApp.getActive().getSheetByName(sheetName);
  var last = sh.getLastRow();
  if (last < 5) return prefix + '-001';
  var ids = sh.getRange(5, col || 1, last - 4, 1).getValues();
  var max = 0;
  for (var i = 0; i < ids.length; i++) {
    var m = String(ids[i][0]).match(/(\d+)$/);
    if (m) max = Math.max(max, parseInt(m[1], 10));
  }
  return prefix + '-' + ('000' + (max + 1)).slice(-3);
}

function firstEmptyRow_(sh) {
  var last = sh.getLastRow();
  return last < 5 ? 5 : last + 1;
}

function prompt_(title, fields) {
  var ui = SpreadsheetApp.getUi();
  var result = {};
  for (var i = 0; i < fields.length; i++) {
    var f = fields[i];
    var resp = ui.prompt(title, f.label, ui.ButtonSet.OK_CANCEL);
    if (resp.getSelectedButton() !== ui.Button.OK) return null;
    result[f.key] = resp.getResponseText();
  }
  return result;
}

function addExpense() {
  var data = prompt_('Add expense', [
    { key: 'desc', label: 'Description (e.g. Island slab deposit)' },
    { key: 'amount', label: 'Amount in USD (e.g. 1860)' },
    { key: 'vendor', label: 'Vendor' },
    { key: 'category', label: 'Category (Labor / Materials / Design / Permits / Delivery / Contingency / Appliances / Furniture / Inspections / Other)' },
    { key: 'status', label: 'Status (Planned / Committed / Paid)' },
    { key: 'room', label: 'Room ID (e.g. RM-01) or leave blank' },
  ]);
  if (!data) return;
  var sh = SpreadsheetApp.getActive().getSheetByName('Expenses');
  var row = firstEmptyRow_(sh);
  var id = nextId_('Expenses', 'EXP');
  sh.getRange(row, 1, 1, 12).setValues([
    [
      id,
      new Date(),
      activeProject_(),
      data.room,
      data.category || 'Other',
      data.vendor,
      data.desc,
      Number(data.amount) || 0,
      'ACH',
      data.status || 'Planned',
      '',
      setting_('Homeowner'),
    ],
  ]);
  toast_('Logged ' + id + ' — ' + data.desc);
}

function addTask() {
  var data = prompt_('Add task', [
    { key: 'title', label: 'Task title' },
    { key: 'room', label: 'Room ID (e.g. RM-01)' },
    { key: 'owner', label: 'Assignee' },
    { key: 'deadline', label: 'Deadline YYYY-MM-DD' },
    { key: 'priority', label: 'Priority (Critical / High / Medium / Low)' },
  ]);
  if (!data) return;
  var sh = SpreadsheetApp.getActive().getSheetByName('Tasks');
  var row = firstEmptyRow_(sh);
  var id = nextId_('Tasks', 'TSK');
  var deadline = data.deadline ? new Date(data.deadline) : '';
  sh.getRange(row, 1, 1, 15).setValues([
    [
      id,
      activeProject_(),
      data.room,
      data.title,
      '',
      data.owner,
      'Homeowner',
      'To Do',
      data.priority || 'Medium',
      new Date(),
      deadline,
      0,
      '',
      0,
      '',
    ],
  ]);
  // copy formula cells if present on row above
  if (row > 5) {
    sh.getRange(row - 1, 16, 1, 2).copyTo(sh.getRange(row, 16, 1, 2));
  }
  toast_('Created ' + id + ' — ' + data.title);
}

function addMaterial() {
  var data = prompt_('Add material', [
    { key: 'product', label: 'Product name' },
    { key: 'sku', label: 'SKU / QR' },
    { key: 'qty', label: 'Quantity required' },
    { key: 'price', label: 'Unit price' },
    { key: 'supplier', label: 'Supplier' },
    { key: 'room', label: 'Room ID' },
  ]);
  if (!data) return;
  var sh = SpreadsheetApp.getActive().getSheetByName('Materials');
  var row = firstEmptyRow_(sh);
  var id = nextId_('Materials', 'MAT');
  sh.getRange(row, 1, 1, 21).setValues([
    [
      id,
      activeProject_(),
      data.room,
      data.product,
      '',
      data.sku,
      'Other',
      Number(data.qty) || 1,
      'ea',
      Number(data.price) || 0,
      '',
      data.supplier,
      0,
      0,
      0,
      'Required',
      0,
      '',
      '',
      '',
      data.sku,
    ],
  ]);
  if (row > 5) {
    sh.getRange(row - 1, 11).copyTo(sh.getRange(row, 11));
    sh.getRange(row - 1, 22).copyTo(sh.getRange(row, 22));
  }
  toast_('Added ' + id + ' — ' + data.product);
}

function addMessage() {
  var data = prompt_('Log a message', [
    { key: 'to', label: 'To (name)' },
    { key: 'room', label: 'Room / task context' },
    { key: 'body', label: 'Message' },
  ]);
  if (!data) return;
  var sh = SpreadsheetApp.getActive().getSheetByName('Messages');
  var row = firstEmptyRow_(sh);
  var id = nextId_('Messages', 'MSG');
  sh.getRange(row, 1, 1, 11).setValues([
    [
      id,
      new Date(),
      activeProject_(),
      data.room,
      setting_('Homeowner'),
      data.to,
      'App',
      data.body,
      '',
      '',
      'No',
    ],
  ]);
  toast_('Message ' + id + ' logged');
}

function refreshShoppingList() {
  var ss = SpreadsheetApp.getActive();
  var shop = ss.getSheetByName('Shopping List');
  if (shop) {
    ss.setActiveSheet(shop);
    SpreadsheetApp.flush();
    toast_('Shopping List uses FILTER of Materials still Required / Quoted / Approved.');
  }
}

function highlightOverdue() {
  var sh = SpreadsheetApp.getActive().getSheetByName('Tasks');
  var last = sh.getLastRow();
  if (last < 5) return;
  var range = sh.getRange(5, 17, last - 4, 1); // Health
  var values = range.getValues();
  var backgrounds = [];
  for (var i = 0; i < values.length; i++) {
    var v = String(values[i][0]);
    if (v === 'Overdue') backgrounds.push([BRAND.danger]);
    else if (v === 'Due Soon') backgrounds.push([BRAND.amber]);
    else if (v === 'Done') backgrounds.push([BRAND.sage]);
    else backgrounds.push([BRAND.ivory]);
  }
  range.setBackgrounds(backgrounds);
  toast_('Overdue tasks highlighted on Tasks!Q');
}

function thisWeekAgenda() {
  var cal = SpreadsheetApp.getActive().getSheetByName('Calendar');
  var last = cal.getLastRow();
  if (last < 5) return;
  var values = cal.getRange(5, 1, last - 4, 7).getValues();
  var today = new Date();
  var end = new Date(today.getTime() + 7 * 86400000);
  var lines = ['This week at Maplewood / Gorge', ''];
  for (var i = 0; i < values.length; i++) {
    var d = values[i][0];
    if (!(d instanceof Date)) continue;
    if (d >= strip_(today) && d <= end) {
      lines.push(
        Utilities.formatDate(d, Session.getScriptTimeZone(), 'EEE d MMM') +
          '  ' +
          values[i][1] +
          '  ·  ' +
          values[i][2] +
          '  ·  ' +
          values[i][5]
      );
    }
  }
  if (lines.length === 2) lines.push('Nothing scheduled in the next 7 days.');
  SpreadsheetApp.getUi().alert(lines.join('\n'));
}

function emailMaintenanceReminders() {
  var sh = SpreadsheetApp.getActive().getSheetByName('Maintenance');
  var last = sh.getLastRow();
  if (last < 5) return;
  var values = sh.getRange(5, 1, last - 4, 14).getValues();
  var due = [];
  for (var i = 0; i < values.length; i++) {
    var flag = String(values[i][13]);
    if (flag.indexOf('OVERDUE') >= 0 || flag.indexOf('Due soon') >= 0) {
      due.push(values[i][1] + ' — ' + values[i][6] + ' (' + flag + ')');
    }
  }
  var email = Session.getActiveUser().getEmail();
  if (!email) {
    SpreadsheetApp.getUi().alert('No user email available in this context.');
    return;
  }
  if (!due.length) {
    toast_('No maintenance items due.');
    return;
  }
  MailApp.sendEmail({
    to: email,
    subject: 'Novality Store — maintenance due',
    htmlBody:
      '<div style="font-family:Georgia,serif;color:#202522">' +
      '<h2 style="color:#16352F">Maintenance due</h2><ul><li>' +
      due.join('</li><li>') +
      '</li></ul></div>',
  });
  toast_('Sent ' + due.length + ' reminder(s) to ' + email);
}

function emailUnreadDigest() {
  var sh = SpreadsheetApp.getActive().getSheetByName('Messages');
  var last = sh.getLastRow();
  if (last < 5) return;
  var values = sh.getRange(5, 1, last - 4, 11).getValues();
  var unread = [];
  for (var i = 0; i < values.length; i++) {
    if (String(values[i][10]) === 'No') {
      unread.push(values[i][4] + ' → ' + values[i][5] + ': ' + values[i][7]);
    }
  }
  var email = Session.getActiveUser().getEmail();
  if (!unread.length) {
    toast_('No unread messages.');
    return;
  }
  MailApp.sendEmail({
    to: email,
    subject: 'Novality Store — unread project messages',
    htmlBody:
      '<div style="font-family:Georgia,serif;color:#202522">' +
      '<h2 style="color:#16352F">Unread messages</h2><ul><li>' +
      unread.join('</li><li>') +
      '</li></ul></div>',
  });
  toast_('Digest sent to ' + email);
}

function toast_(msg) {
  SpreadsheetApp.getActive().toast(msg, 'Novality Store', 6);
}

function strip_(d) {
  return new Date(d.getFullYear(), d.getMonth(), d.getDate());
}
