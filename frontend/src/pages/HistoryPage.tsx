
import {
  BookOpen,
  History,
  MessageCircle,
  RefreshCcw,
} from "lucide-react";

import {
  useEffect,
  useState,
} from "react";

import {
  Link,
} from "react-router";

import {
  getStudentChatHistory,
} from "../api/history";

import type {
  SessionHistorySummary,
} from "../types/history";

import {
  getStoredStudent,
} from "../utils/studentStorage";


function getSessionUrl(
  session: SessionHistorySummary,
): string {

  const subject = session.subject.toLowerCase();

  return `/learn/${subject}/session/${session.session_id}`;
}


function formatDate(value: string): string {

  const timestamp =
    value.endsWith("Z")
    || /[+-]\d{2}:\d{2}$/.test(value)
      ? value
      : `${value}Z`;

  const date = new Date(timestamp);

  if (Number.isNaN(date.getTime())) {
    return "Unknown date";
  }

  return date.toLocaleString();
}


export default function HistoryPage() {

  const student = getStoredStudent();

  const [sessions, setSessions] = useState<
    SessionHistorySummary[]
  >([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState<
    string | null
  >(null);

  const [refreshKey, setRefreshKey] = useState(0);


  useEffect(() => {

    const studentId = student?.id;

    if (!studentId) {
      setLoading(false);
      return;
    }

    let active = true;

    async function loadHistory() {

      setLoading(true);
      setError(null);

      try {

        const data =
          await getStudentChatHistory(studentId!);

        if (active) {
          setSessions(data);
        }

      } catch (err) {

        if (active) {
          setError(
            err instanceof Error
              ? err.message
              : "Unable to load learning history."
          );
        }

      } finally {

        if (active) {
          setLoading(false);
        }
      }
    }

    void loadHistory();

    return () => {
      active = false;
    };

  }, [student?.id, refreshKey]);


  return (

    <div className="history-page">

      <div className="history-heading">

        <div>

          <div className="history-eyebrow">
            <History size={18} />
            <span>Learning history</span>
          </div>

          <h1>Conversation History</h1>

          <p>
            Review your previous lessons and
            continue learning where you left off.
          </p>

        </div>


        <button
          type="button"
          className="history-refresh"
          onClick={() =>
            setRefreshKey((prev) => prev + 1)
          }
        >
          <RefreshCcw size={17} />
          Refresh
        </button>

      </div>


      {loading && (
        <p className="history-notice">
          Loading conversations...
        </p>
      )}


      {error && (
        <div
          className="history-notice history-error"
          role="alert"
        >
          {error}
        </div>
      )}


      {!loading && !error && sessions.length === 0 && (

        <div className="history-empty surface-card">

          <BookOpen size={35} />

          <h2>No conversation history yet</h2>

          <p>
            Start learning Math, Science, or English.
            Your conversations will appear here.
          </p>

          <Link
            to="/learn"
            className="history-start-link"
          >
            Start Learning
          </Link>

        </div>

      )}


      {!loading && !error && sessions.length > 0 && (

        <div className="history-list">

          {sessions.map((session) => (

            <Link
              key={session.session_id}
              to={getSessionUrl(session)}
              className="history-session surface-card"
            >

              <div className="history-session-icon">
                <MessageCircle size={22} />
              </div>

              <div className="history-session-content">

                <div className="history-session-meta">

                  <span className="history-subject">
                    {session.subject.toLowerCase()}
                  </span>

                  <span>
                    {formatDate(session.last_message_at)}
                  </span>

                </div>

                <h2>
                  {session.topic ?? session.subject}
                </h2>

                <p>
                  {session.last_message_preview}
                </p>

                <small>
                  {session.message_count} messages
                </small>

              </div>

              <span className="history-resume">
                Resume →
              </span>

            </Link>

          ))}

        </div>

      )}

    </div>
  );
}
