
import {
  ClipboardCheck,
  Trophy,
} from "lucide-react";


interface AssessmentScore {
  score_percent: number;
}


interface Props {
  subject: "Math" | "Science";

  diagnostic: AssessmentScore | null | undefined;
  mastery: AssessmentScore | null | undefined;

  onDiagnostic: () => void;
  onMastery: () => void;

  error?: string | null;
}


export default function AssessmentProgressCard({
  subject,
  diagnostic,
  mastery,
  onDiagnostic,
  onMastery,
  error = null,
}: Props) {

  const scoreGain =
    diagnostic && mastery
      ? mastery.score_percent - diagnostic.score_percent
      : null;

  const scoreText = (
    score: AssessmentScore | null | undefined,
  ): string => {
    if (error) return "Unavailable";
    return score
      ? `${score.score_percent}%`
      : "Not taken";
  };


  return (
    <section className="surface-card progress-detail-card">

      <div className="progress-card-heading">
        <div>
          <span className="small-label">
            {subject.toUpperCase()} ASSESSMENTS
          </span>

          <h2>Diagnostic and Mastery</h2>
        </div>

        <ClipboardCheck size={27} />
      </div>


      <div className="progress-stats">

        <div>
          <strong>{scoreText(diagnostic)}</strong>
          <span>Diagnostic score</span>
        </div>

        <div>
          <strong>{scoreText(mastery)}</strong>
          <span>Mastery score</span>
        </div>

        <div>
          <strong>
            {error || scoreGain === null
              ? "—"
              : `${scoreGain > 0 ? "+" : ""}${scoreGain.toFixed(2)}`}
          </strong>

          <span>Change (percentage points)</span>
        </div>

      </div>


      {error && (
        <p role="status" style={{ marginTop: 14 }}>
          Assessment results are temporarily
          unavailable: {error}
        </p>
      )}


      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: 12,
          marginTop: 24,
        }}
      >

        <button
          type="button"
          className="secondary-button"
          onClick={onDiagnostic}
        >
          <ClipboardCheck size={17} />
          Take Diagnostic
        </button>

        <button
          type="button"
          className="primary-button"
          onClick={onMastery}
        >
          <Trophy size={17} />
          Take Mastery Check
        </button>

      </div>

    </section>
  );
}
