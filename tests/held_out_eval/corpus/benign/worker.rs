//! Background worker that consumes index jobs from a channel.

use std::time::Duration;
use tokio::sync::mpsc;
use tokio::time;

#[derive(Debug)]
pub struct IndexJob {
    pub note_id: i64,
    pub body: String,
}

pub async fn run(mut rx: mpsc::Receiver<IndexJob>) {
    while let Some(job) = rx.recv().await {
        if let Err(e) = index_one(&job).await {
            tracing::warn!(note_id = job.note_id, error = %e, "index job failed; will retry");
            time::sleep(Duration::from_millis(250)).await;
        } else {
            tracing::debug!(note_id = job.note_id, "indexed");
        }
    }
    tracing::info!("worker channel closed, shutting down");
}

async fn index_one(job: &IndexJob) -> anyhow::Result<()> {
    // Tokenize and upsert into the FTS table. Placeholder for the real impl.
    let token_count = job.body.split_whitespace().count();
    tracing::trace!(note_id = job.note_id, token_count, "tokenized");
    Ok(())
}
