import little_mallet_wrapper as lmw
import sys

MALLET_PATH = "~/mallet/bin/mallet"


def lmw_training(num_topics, output_directory_path, training_data): 
    '''
    Training a topic model using little_mallet_wrapper
    Saving output to designated output directory
    '''
    path_to_training_data           = output_directory_path + '/training.txt'
    path_to_formatted_training_data = output_directory_path + '/mallet.training'
    path_to_model                   = output_directory_path + '/mallet.model.' + str(num_topics)
    path_to_topic_keys              = output_directory_path + '/mallet.topic_keys.' + str(num_topics)
    path_to_topic_distributions     = output_directory_path + '/mallet.topic_distributions.' + str(num_topics)
    path_to_word_weights            = output_directory_path + '/mallet.word_weights.' + str(num_topics)
    path_to_diagnostics             = output_directory_path + '/mallet.diagnostics.' + str(num_topics) + '.xml'

    lmw.import_data(MALLET_PATH, path_to_training_data,
                    path_to_formatted_training_data,
                    training_data)

    lmw.train_topic_model(MALLET_PATH,
                        path_to_formatted_training_data,
                        path_to_model,
                        path_to_topic_keys,
                        path_to_topic_distributions,
                        path_to_word_weights,
                        path_to_diagnostics,
                        num_topics)

