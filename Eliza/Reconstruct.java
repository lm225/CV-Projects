import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Random;

public class Reconstruct {

	public boolean reconstructSentence(String[] words) throws IOException{
		PostSubRules postsub = new PostSubRules();	

		boolean output = false;

		try{
			BufferedReader reader = new BufferedReader(new FileReader(
					"script.txt"));
			String reassemble;

			//uses post-sub method and the user's input to construct a sentence
			//looks for a word...
			for(int i = 0; i < words.length; i ++){
				//...if it is a possible post-sub, call this method...
				if(postsub.postSubRules(words, i) == true){
					//...then look through the remaining words...
					for(int j = 1; j < words.length; j++){
						//...and check for post-subs again
						if(postsub.postSubRules(words, j) == false){
							//prints out each word in turn
							System.out.print(words[j] + " ");
							output = true;

						}
					}
				} else output = false;

				if (output == true){
					//read each line of the script (to the end)
					while ((reassemble = reader.readLine()) != null) {
						String[] response = reassemble.split("::");
						//check that the first character of the line is a 6
						if (reassemble.charAt(0) == ('6')) {
							//generate a random number to give a random response
							int r = 0;
							while(r < 1){
								Random random = new Random();
								r = random.nextInt(response.length);
							}
							System.out.print(response[r]);
						}	

					}Eliza e = new Eliza();
					e.start();
				}

			}}

		catch(FileNotFoundException e){
			System.out.println("The File Specified Could Not Be Found");
		}
		return output;
	}

}
