// calendar_probe.swift — Wednesday dashboard: read-only EventKit probe.
// Lists calendars and today's+tomorrow's events as JSON. NEVER writes.
// First run triggers the macOS calendar-access prompt (one-time, per app host).
import EventKit
import Foundation

let store = EKEventStore()
let sem = DispatchSemaphore(value: 0)
var granted = false

if #available(macOS 14.0, *) {
    store.requestFullAccessToEvents { ok, _ in granted = ok; sem.signal() }
} else {
    store.requestAccess(to: .event) { ok, _ in granted = ok; sem.signal() }
}
sem.wait()

guard granted else {
    print("{\"error\": \"calendar access DENIED — grant in System Settings > Privacy & Security > Calendars\"}")
    exit(1)
}

let cals = store.calendars(for: .event)
let fmt = ISO8601DateFormatter()
let start = Calendar.current.startOfDay(for: Date())
let end = Calendar.current.date(byAdding: .day, value: 8, to: start)!
let pred = store.predicateForEvents(withStart: start, end: end, calendars: nil)
let events = store.events(matching: pred).sorted { $0.startDate < $1.startDate }

func esc(_ s: String) -> String {
    s.replacingOccurrences(of: "\\", with: "\\\\").replacingOccurrences(of: "\"", with: "\\\"")
}

var out = "{\"calendars\": ["
out += cals.map { "{\"title\": \"\(esc($0.title))\", \"account\": \"\(esc($0.source?.title ?? "?"))\"}" }.joined(separator: ", ")
out += "], \"events_next_48h\": ["
out += events.map {
    "{\"cal\": \"\(esc($0.calendar.title))\", \"title\": \"\(esc($0.title ?? ""))\", \"start\": \"\(fmt.string(from: $0.startDate))\", \"allday\": \($0.isAllDay)}"
}.joined(separator: ", ")
out += "]}"
print(out)
