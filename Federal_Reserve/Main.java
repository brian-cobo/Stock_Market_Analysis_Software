package com.brian.cobo;

import java.io.IOException;
import java.util.*;
import java.nio.file.*;
import java.io.File;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;
import static java.util.stream.Collectors.*;
import static java.util.Map.Entry.*;
import java.text.ParseException;
import java.util.concurrent.TimeUnit;
import java.math.RoundingMode;
import java.text.DecimalFormat;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Main {

    public static void main(String[] args) throws IOException, ParseException
    {

        long startTime = System.currentTimeMillis();
        String article_paths = "/Users/brian/Desktop/Programming/Python Workspace/Stock_Market_Analysis_Software/Federal_Reserve/Articles/";
        List<String> all_files = get_all_articles(article_paths);
        for (int i=0; i < all_files.size(); i++)
        {
            List<String> article = load_article_into_array(all_files.get(i));
            List<String> filtered_article = filter_out_stopwords(article);
            create_ngrams(filtered_article);
        }

        print_execution_time(startTime);


    }

    public static List<String> get_all_articles(String path) throws IOException {
        try (Stream<Path> walk = Files.walk(Paths.get(path)))
        {
            List<String> file = walk.map(x -> x.toString())
                    .filter(f -> f.endsWith(".txt")).collect(Collectors.toList());
            return file;
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
        return null;
    }

    public static void print_execution_time(long startTime)
    {
        DecimalFormat df = new DecimalFormat("0.00");
        long stopTime = System.currentTimeMillis();
        long elapseTimeMin = (stopTime - startTime)/60000;
        double elapsedTimeSec = ((stopTime - startTime)/1000.0);
        System.out.println("Execution Time: " + elapseTimeMin + "m " + df.format(elapsedTimeSec)+ "s");
    }

    public static List<String> load_article_into_array(String filepath) throws IOException
    {
        String article = new String(Files.readAllBytes(Paths.get(filepath)));
        String[] parsed_article_array = article.replaceAll("[^a-zA-Z\n ]", "").toLowerCase().split("\\s+");
        List<String> parsed_article = new ArrayList(Arrays.asList(parsed_article_array));

        return parsed_article;
    }

    public static List<String> filter_out_stopwords(List<String> article)
    {
        String[] stop_words_array = {"a", "about", "above", "after", "again", "against", "all",
                                     "am", "an", "and", "any", "are", "as", "at", "be", "because",
                                     "been", "before", "being", "below", "between", "both", "but",
                                     "by", "can", "did", "do", "does", "doing", "don", "down", "during",
                                     "each", "few", "for", "from", "further", "had", "has", "have", "having",
                                     "he", "her", "here", "hers", "herself", "him", "himself", "his", "how",
                                     "i", "if", "in", "into", "is", "it", "its", "itself", "just", "me", "more",
                                     "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on", "once",
                                     "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "s",
                                     "same", "she", "should", "so", "some", "such", "t", "than", "that", "the",
                                     "their", "theirs", "them", "themselves", "then", "there", "these", "they",
                                     "this", "those", "through", "to", "too", "under", "until", "up", "very", "was",
                                     "we", "were", "what", "when", "where", "which", "while", "who", "whom", "why",
                                     "will", "with", "you", "your", "yours", "yourself", "yourselves"};


        List<String> stopwords = Arrays.asList(stop_words_array);
        for (int i=0; i < article.size(); i++)
            if(stopwords.contains(article.get(i)))
                article.remove(i);
        return article;
    }

    public static void create_ngrams(List <String> parsed_article)
    {
        Map<String, Integer> unigram = create_ngram_n_1(parsed_article);
        Map<String, Integer> bigram = create_ngram_n_2(parsed_article);
        Map<String, Integer> trigram = create_ngram_n_3(parsed_article);
        Map<String, Integer> quadgram = create_ngram_n_4(parsed_article);
        Map<String, Integer> quintgram = create_ngram_n_5(parsed_article);
    }

    public static Map<String, Integer> sort_ngrams(Map <String, Integer> ngrams)
    {
        Map<String, Integer> sorted_ngrams = ngrams
                .entrySet()
                .stream()
                .sorted(Collections.reverseOrder(Map.Entry.comparingByValue()))
                .collect(
                        toMap(e -> e.getKey(), e -> e.getValue(), (e1, e2) -> e2,
                                LinkedHashMap::new));
        return sorted_ngrams;
    }

    public static Map<String, Integer> create_ngram_n_1(List <String> parsed_article)
    {
        Map<String, Integer> unigram = new HashMap<String, Integer>();
        for (int word=0; word < parsed_article.size(); word++)
        {
            if (unigram.get(parsed_article.get(word)) == null)
                unigram.put(parsed_article.get(word), 1);
            else
                unigram.put(parsed_article.get(word), unigram.get(parsed_article.get(word)) + 1);
        }
        Map<String, Integer> sorted_unigrams = sort_ngrams(unigram);
        return sorted_unigrams;
    }

    public static Map<String, Integer> create_ngram_n_2(List <String> parsed_article)
    {
        Map<String, Integer> ngram = new HashMap<String, Integer>();
        for (int word=0; word < parsed_article.size()-1; word++)
        {
            if (parsed_article.get(word + 1) != null)
            {
                String bigram = parsed_article.get(word) + " " + parsed_article.get(word + 1);
                if (ngram.get(bigram) == null)
                    ngram.put(bigram, 1);
                else
                    ngram.put(bigram, ngram.get(bigram) + 1);
            }
        }
        Map<String, Integer> sorted_bigrams = sort_ngrams(ngram);
        return sorted_bigrams;
    }

    public static Map<String, Integer> create_ngram_n_3(List <String> parsed_article)
    {
        Map<String, Integer> ngram = new HashMap<String, Integer>();
        for (int word=0; word < parsed_article.size()-2; word++)
        {
            if (parsed_article.get(word + 2) != null)
            {
                String trigram = (parsed_article.get(word) + " " +
                                  parsed_article.get(word + 1) + " " +
                                  parsed_article.get(word + 2));
                if (ngram.get(trigram) == null)
                    ngram.put(trigram, 1);
                else
                    ngram.put(trigram, ngram.get(trigram) + 1);
            }
        }
        Map<String, Integer> sorted_trigrams = sort_ngrams(ngram);
        return sorted_trigrams;
    }

    public static Map<String, Integer> create_ngram_n_4(List <String> parsed_article)
    {
        Map<String, Integer> ngram = new HashMap<String, Integer>();
        for (int word=0; word < parsed_article.size()-3; word++)
        {
            if (parsed_article.get(word + 3) != null)
            {
                String quadgram = (parsed_article.get(word) + " " +
                        parsed_article.get(word + 1) + " " +
                        parsed_article.get(word + 2) + " " +
                        parsed_article.get(word + 3));
                if (ngram.get(quadgram) == null)
                    ngram.put(quadgram, 1);
                else
                    ngram.put(quadgram, ngram.get(quadgram) + 1);
            }
        }
        Map<String, Integer> sorted_quadgrams = sort_ngrams(ngram);
        return sorted_quadgrams;
    }

    public static Map<String, Integer> create_ngram_n_5(List <String> parsed_article)
    {
        Map<String, Integer> ngram = new HashMap<String, Integer>();
        for (int word=0; word < parsed_article.size()-4; word++)
        {
            if (parsed_article.get(word + 4) != null)
            {
                String quingram = (parsed_article.get(word) + " " +
                        parsed_article.get(word + 1) + " " +
                        parsed_article.get(word + 2) + " " +
                        parsed_article.get(word + 3) + " " +
                        parsed_article.get(word + 4));
                if (ngram.get(quingram) == null)
                    ngram.put(quingram, 1);
                else
                    ngram.put(quingram, ngram.get(quingram) + 1);
            }
        }
        Map<String, Integer> sorted_quingrams = sort_ngrams(ngram);
        return sorted_quingrams;
    }



}
