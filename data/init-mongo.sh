#!/bin/bash

# Wait for MongoDB to be ready
until mongosh --host $MONGO_HOST --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase $MONGO_ACCESS --eval "print(\"waited for connection\")"
do
    sleep 5
done

# Check if the collection is empty
count=($(mongosh --host $MONGO_HOST --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase $MONGO_ACCESS  --eval "use $MONGO_DB;" --eval "db.$MONGO_COLLECTION.countDocuments();"))
if [ "$count" -gt 0 ]; then
    echo "Collection is not empty. Skipping import."
else
    echo "Collection is empty. Importing data..."
    # Run the mongoimport command
    mongoimport --uri $ME_CONFIG_MONGODB_URL --authenticationDatabase=$MONGO_ACCESS --db $MONGO_DB --collection $MONGO_COLLECTION --type csv --headerline --file $DATA_FILE_PATH
fi