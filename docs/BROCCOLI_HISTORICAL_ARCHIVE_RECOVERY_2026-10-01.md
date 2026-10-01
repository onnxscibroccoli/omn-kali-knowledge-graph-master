# Broccoli historical archive recovery evidence - 2026-10-01

Source checked: onnxscibroccoli/broccoli-core main at e8eff124000e8bfb0a9419281d065a493d880cc5.

RECOVERED_HISTORICAL:
- tools/broccoli_conv_archive.py is a real conversation archive.
- It writes compressed JSONL under ~/broccoli/archive/conversations.
- It creates ~/broccoli/archive/index.sqlite.
- SQLite tables are conv(id, ts, src, path, sha, bytes, prev) and lookup(kw, cid).
- Inputs include ~/broccoli/inbox/grok_reply.txt and /sdcard/Broccoli/pull/bundle_*.
- SHA-256 is used for deduplication.
- runtime/account_pool.py provides provider-neutral account identity and rotation.

RECOVERED_HISTORICAL_HARVEST:
- modules/chat_harvest.py
- modules/chat_nav.py
- modules/chat_reader.py
- modules/chat_store.py
The old navigation explicitly remained current-thread-only, so all-provider/all-chat traversal was not proven complete.

RECOVERED_HISTORICAL_STORAGE:
- Agent/Broccoli/mirror/meta/broccoli_storage_sync.py
- tools/broccoli_storage_healer.sh
- sync_checkpoint.sh
These show shared-storage mirroring, bounded sync, storage protection, and checkpoint conventions.

CURRENT_ADOPTION:
- Grasshopper keeps immutable page artifacts as source of truth.
- SQLite/FTS is derived and rebuildable.
- Provider + account + conversation + message is the normalized identity chain.
- Project/workspace membership is metadata.
- Protected content is quarantined before FTS.
- /sdcard/OmniKali/broccoli/archive-journal is the new durable namespace.
- Historical /sdcard/Broccoli/pull remains a compatibility input.

Evidence vocabulary:
PROVEN_HISTORICAL means source code exists in the historical repo.
NOT_PROVEN means the historical implementation did not prove provider completeness, Android kill recovery, or production acceptance.
